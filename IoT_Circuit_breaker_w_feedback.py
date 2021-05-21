# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  switch_origin = [0.065, 0, -0.01, 0.7071, 0.7071, 0.0, 0.0]
  last_reset = False
  activated = True
  overload = False
  x2_voltage = [0.0, 0.0, 0.0]
  x4_voltage = [0.0, 0.0, 0.0]
  x1_current = [0.0, 0.0, 0.0]
  x3_current = [0.0, 0.0, 0.0]
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"

# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<l1_voltage[0]-l0_voltage[0]<30
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
      # Check user action "on_clicked" to switch state and reset overload    
      if activated:
        send_value = "TRUE"
      else:
        send_value = "FALSE"
      # Send data to the driver
      update_input = json.dumps({topic: send_value})

  # Driver Error
  elif sensor_state == 4:
    enable_driver = False
    
  # Component behavior
  if not last_reset and reset:
    activated = not activated
    overload = False
  last_reset = reset

  # Check max current to set overload
  if x2_current[0]>max_current:
    overload = True
    activated = False
    
  # Check if reset
  if activated:
    switch_origin =  [0.065, 0, -0.005, 0.5, 0.5, 0.5, 0.5]
    x2_voltage = x1_voltage
    x4_voltage = x3_voltage
    x1_current = x2_current
    x3_current = x4_current
  else:
    switch_origin = [0.065, 0, -0.01, 0.7071, 0.7071, 0.0, 0.0]
    x2_voltage = x4_voltage = x3_current = x1_current = [0.0, 0.0, 0.0]
