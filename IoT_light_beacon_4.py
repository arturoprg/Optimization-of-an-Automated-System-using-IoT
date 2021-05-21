# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  actuator_state = 0
  setup_data = "{}"
  actuator_value = "Off"
  x2_current = [0.0, 0.0, 0.0]
  light1_current = 0.0
  light2_current = 0.0
  light3_current = 0.0
  light4_current = 0.0
  light1_color = [0, 0, 0.1, 1]
  light2_color = [0, 0.1, 0, 1]
  light3_color = [0.1, 0.1, 0, 1]
  light4_color = [0.1, 0, 0, 1]
  n_current = 0.01
# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 220<(x1_voltage[0]-x2_voltage[0])<240
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    light2_color = [0, 0.1, 0, 1]
    light1_color = [0, 0, 0.1, 1]
    light3_color = [0.1, 0.1, 0, 1]
    light4_color = [0.1, 0, 0, 1]
    light1_current = light2_current = light3_current = light4_current = 0.0
    actuator_state = 0
   
  # Sensor powered off
  if actuator_state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    step_time = 0
    
    # Powered on
    if in_voltage_ok:
      actuator_state = 1
      step_time = 0.1
            
  # Power up and Setup driver connection
  elif actuator_state == 1:    
    # Setup data to send
    setup_dict = {
      'parameters': {
        'ip':ip_address
      },
      'variables': {
        topic: {'datatype': 'str', 'size': 1, 'operation': 'read'},
      }
    }
    setup_data = json.dumps(setup_dict)
    actuator_state = 2
            
  # Driver connecting
  elif actuator_state == 2:
    # Enable driver, wait for response
    enable_driver = True
    if driver_status == 'RUNNING':
      actuator_state = 3
            	
  # Driver ready and running
  elif actuator_state == 3:
    # Error if connection lost
    step_time = 0
    if driver_status != 'RUNNING':
        actuator_state = 4
    else:
        update_output_json = json.loads(update_output)
        if topic in update_output_json:
            actuator_value = update_output_json[topic].lower()
          
        if actuator_value == "blue on":
          light1_color = [0.3, 0.3, 1, 1]
          # Apply current
          light1_current = n_current
        
        elif actuator_value == "blue off":
          light1_color = [0, 0, 0.1, 1]
          light1_current = 0.0
          
        elif actuator_value == "green on":
          # Switch on green light
          light2_color = [0.1, 1, 0.1, 1]
          # Apply current
          light2_current = n_current
        
        elif actuator_value == "green off":
          light2_color = [0, 0.1, 0, 1]
          light2_current = 0.0
          
        elif actuator_value == "yellow on":
          # Switch on yellow light
          light3_color = [1, 1, 0.1, 1]
          # Apply current
          light3_current = n_current
          
        elif actuator_value == "yellow off":
          light3_color = [0.1, 0.1, 0, 1]
          light3_current = 0.0
          
        elif actuator_value == "red on":
          # Switch on red light
          light4_color = [1, 0.1, 0.1, 1]
          # Apply current
          light4_current = n_current
          
        elif actuator_value == "red off":
          light4_color = [0.1, 0, 0, 1]
          light4_current = 0.0
  
  # Driver Error
  elif actuator_state == 4:
    enable_driver = False
    
  x2_current = [-light1_current - light2_current - light3_current - light4_current, 50, x1_voltage[2]]
  x1_current = [-x2_current[0],x2_current[1],x2_current[2]]