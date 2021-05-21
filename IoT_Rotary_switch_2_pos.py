# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  button_frame = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"
  switch_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.3827, 0.9239]
  last_pressed = False
  state_1 = True

# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<(x1_voltage[0]-x0_voltage[0])<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    sensor_state = 0
   
  # Sensor powered off
  if sensor_state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    update_input = "{}"
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
        topic: {'datatype': 'bool', 'size': 1, 'operation': 'write'},
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
      if state_1:
        sensor_value = "TRUE"
      else:
        sensor_value = "FALSE"
      # Send data to the driver
      update_input = json.dumps({topic: sensor_value})

  # Driver Error
  elif sensor_state == 4:
    enable_driver = False
    
#Component behavior
  if not last_pressed and switch_pressed:
    state_1 = not state_1
  if state_1:
    switch_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.3827, 0.9239]
  else:
    switch_pos = [0.0, 0.0, 0.0, 0.0, 0.0, -0.3827, 0.9239]
  last_pressed = switch_pressed