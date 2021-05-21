# The code bellow is executed just when the function is initialized
if initialize:
    # Initialize outputs
    l1_out_voltage = [0.0, 0.0, 0.0]
    l2_out_voltage = [0.0, 0.0, 0.0]
    l3_out_voltage = [0.0, 0.0, 0.0]
    l1_in_current = [0.0, 0.0, 0.0]
    l2_in_current = [0.0, 0.0, 0.0]
    l3_in_current = [0.0, 0.0, 0.0]
    actuator_state = 0
    setup_data = "{}"
    actuator_value = "None"
# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<(x1_voltage[0]-x0_voltage[0])<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
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
      update_output_json = json.loads(update_output_script)
      if topic in update_output_json:
          actuator_value = update_output_json[topic]
        
      if actuator_value == "Fwd":
          l1_out_voltage = l1_in_voltage
          l2_out_voltage = l2_in_voltage
          l3_out_voltage = l3_in_voltage
          l1_in_current = l1_out_current
          l2_in_current = l2_out_current
          l3_in_current = l3_out_current
      elif actuator_value == "Rev":
          l1_out_voltage = l1_in_voltage
          l2_out_voltage = l3_in_voltage
          l3_out_voltage = l2_in_voltage
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
    
  elif actuator_state == 4:
      enable_driver = False