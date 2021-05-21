if initialize:
    # Outputs
    l1_out_voltage = [0.0, 0.0, 0.0]
    l2_out_voltage = [0.0, 0.0, 0.0]
    l3_out_voltage = [0.0, 0.0, 0.0]
    l1_in_current = [0.0, 0.0, 0.0]
    l2_in_current = [0.0, 0.0, 0.0]
    l3_in_current = [0.0, 0.0, 0.0]
    kW = 0.0
    # Internal variables
    sensor_state = 0
    setup_data = "{}"
    update_input = "{}"
	
else:
  # Sensor powered off
  if sensor_state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    update_input = "{}"
    step_time = 0
    sensor_state = 1
    step_time = 0.1
            
  # Power up and Setup driver connection
  elif sensor_state == 1:    
    # Setup data to send
    setup_dict = {
      'parameters': {
        'ip':ip_address
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
      # If we have a current on all three outputs we can use
      # the three phase line-to-line power equation
      if (l1_out_current[0] > 0 and 
          l2_out_current[0] > 0 and 
          l3_out_current[0] > 0):
      # sqrt( (V1 x C1 x sqrt(3))^2 + (V2 x C2 x sqrt(3))^2 + (V3 x C3 x sqrt(3))^2 )
        kW = ((((l1_in_voltage[0] * l1_out_current[0]) * 3 ** 0.5) ** 2 +
            ((l1_in_voltage[0] * l1_out_current[0]) * 3 ** 0.5) ** 2 +
            ((l1_in_voltage[0] * l1_out_current[0]) * 3 ** 0.5) ** 2 ) ** 0.5)/1000

      else:
        kW = ((l1_in_voltage[0] * l1_out_current[0]) +
            (l1_in_voltage[0] * l1_out_current[0])  +
            (l1_in_voltage[0] * l1_out_current[0]))/1000

      update_input = json.dumps({topic: kW})
  
  elif sensor_state == 4:
    enable_driver = False
      
  # Let voltage pass-through
  l1_out_voltage = l1_in_voltage
  l2_out_voltage = l2_in_voltage
  l3_out_voltage = l3_in_voltage
  # Let current pass-through
  l1_in_current = l1_out_current
  l2_in_current = l2_out_current
  l3_in_current = l3_out_current