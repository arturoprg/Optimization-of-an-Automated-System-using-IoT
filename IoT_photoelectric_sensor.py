# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  signal_voltage = [0, 0, 0]
  ray_color = [0.9, 0.9, 0.0, 1.0]
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"

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
        topic: {'datatype': 'str', 'size': 1, 'operation': 'write'},
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
      if sensor_status:
        sensor_value = True
        ray_color = [0.0, 0.8, 0.0, 1.0]
      else:
        sensor_value = False
        ray_color = [0.9, 0.9, 0.0, 1.0]

      if sensor_value:
        send_value = "TRUE"
      else:
        send_value = "FALSE"
      # Send data to the driver
      update_input = json.dumps({topic: send_value})

  # Driver Error
  elif sensor_state == 4:
    enable_driver = False