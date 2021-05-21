# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  # NOTE: All visuals has to have the origin in the same
  # place for the transformations to work properly
  rotation_transform = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
  [x, y, z, R, P, Y] = Transform2Euler(rotation_transform)
  # The limits of yaw rotation
  Y_range = [0.0, 0.55 * numpy.pi]
  # The angular velocity when rotating [rad/s]
  Y_movement_vel = 0.5
  # Direction of movement (1 for opening, -1 for closing)
  Y_movement_dir = 0.0
  closed = True
  locked = False
  last_clock = clock
  step_time = 0.0
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"
  actuator_value = "False"
  last_value = "False"
  done = False
  
# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<(x1_voltage[0]-x2_voltage[0])<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    sensor_state = 0
   
  # Sensor powered off
  if sensor_state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    update_input = "{}"
    sensor_value = False
    step_time = 0
    
    # Powered on
    if in_voltage_ok:
      sensor_state = 1
      step_time = 0.1
            
  # Power up and Setup driver connection
  elif sensor_state == 1:    
    # Setup data to send
    setup_dict = {
      'parameters': {
        'ip':ip_address,
        'force_write':0
      },
      'variables': {
        topicPub: {'datatype': 'str', 'size': 1, 'operation': 'write'},
        topicSub: {'datatype': 'str', 'size': 1, 'operation': 'read'},
      }
    }
    setup_data = json.dumps(setup_dict)
    sensor_state = 2
            
  # Driver connecting
  elif sensor_state == 2:
    # Enable driver, wait for response
    enable_driver = True
    if driver_status == 'RUNNING':
      sensor_state = 3
            	
  # Driver ready and running
  elif sensor_state == 3:
    # Error if connection lost
    step_time = 0
    if driver_status != 'RUNNING':
      sensor_state = 4
    else:
      # Read the topic
      update_output_json = json.loads(update_output)
      if topicSub in update_output_json:
        actuator_value = update_output_json[topicSub].lower()
        
      # Only accept user action when we are not rotating
      if handle_pressed and Y_movement_dir == 0.0:
        if closed and not locked:
          # Start opening door
          Y_movement_dir = 1.0
          closed = False
        elif not closed:
          # Start closing door
          Y_movement_dir = -1.0
    
      # Only do the transform calculations if we are actually moving
      elif Y_movement_dir != 0.0:
        dt = clock - last_clock
        Y += numpy.pi * Y_movement_vel * Y_movement_dir * dt
        
        # Check if we reached a limit, in that case stop rotating
        if Y <= Y_range[0] and Y_movement_dir < 0:
            Y = Y_range[0]
            Y_movement_dir = 0.0
            closed = True
        elif Y >= Y_range[1] and Y_movement_dir > 0:
            Y = Y_range[1]
            Y_movement_dir = 0.0

        rotation_transform = Transform2Quat([x, y, z, R, P, Y])
    
      # Check if we have a supply voltage difference > 20V
      if x1_voltage[0] - x2_voltage[0] > 20:
        # By only changing locked state here, the door keeps
        # being locked if the power is lost (fail secure)
        locked = False if (actuator_value == "unlock") else True
     	
      last_clock = clock
      step_time = 0.01 if Y_movement_dir != 0.0 else 0.0
        
      # Write in the Topic
      lock_value = "L" if (closed and locked) else "U" 
      open_value = "TRUE" if closed else "FALSE" 
      send_value = lock_value+open_value
      update_input = json.dumps({topicPub: send_value})
      


  # Driver Error
  elif sensor_state == 4:
    enable_driver = False