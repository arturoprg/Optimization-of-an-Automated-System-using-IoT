# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  l1_out_voltage = [0.0, 0.0, 0.0]
  l2_out_voltage = [0.0, 0.0, 0.0]
  l3_out_voltage = [0.0, 0.0, 0.0]
  l1_in_current = [0.0, 0.0, 0.0]
  l2_in_current = [0.0, 0.0, 0.0]
  l3_in_current = [0.0, 0.0, 0.0]
  switch_pos = [0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.7071]
  connection_closed = True
  last_pressed = False
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"
  send_value = "False"
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
        topic: {'datatype': 'str', 'size': 1, 'operation': 'write'},
      }
    }
    setup_data = json.dumps(setup_dict)
    sensor_state = 2
            
  # Driver connecting
  elif sensor_state == 2:
    # Enable driver, wait for response
    enable_driver = True
    update_input = json.dumps({topic: send_value})
    if driver_status == 'RUNNING':
      sensor_state = 3
            	
  # Driver ready and running
  elif sensor_state == 3:
    # Error if connection lost
    step_time = 0
    if driver_status != 'RUNNING':
      sensor_state = 4
    
    else:
      if connection_closed:
        send_value = "TRUE"
      else:
        send_value = "FALSE"
      
      update_input = json.dumps({topic: send_value})

  # Driver Error
  elif sensor_state == 4:
    enable_driver = False
    
  # Component behavior   
  # Check if the switch has been released and pressed again
  if not last_pressed and switch_pressed:
    # Change state of the connection
    connection_closed = not connection_closed
        
  last_pressed = switch_pressed
        
  # Update switch position
  if connection_closed:
    switch_pos = [0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.7071]
  else:
    switch_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1]
        
  # Pass the input values through if connection is closed
  # Otherwise, put 0 to all outputs
  if connection_closed:
    l1_out_voltage = l1_in_voltage
    l2_out_voltage = l2_in_voltage
    l3_out_voltage = l3_in_voltage
    l1_in_current = l1_out_current
    l2_in_current = l2_out_current
    l3_in_current = l3_out_current

  else:
    l1_out_voltage = [0.0, 0.0, 0.0]
    l2_out_voltage = [0.0, 0.0, 0.0]
    l3_out_voltage = [0.0, 0.0, 0.0]
    l1_in_current = [0.0, 0.0, 0.0]
    l2_in_current = [0.0, 0.0, 0.0]
    l3_in_current = [0.0, 0.0, 0.0]