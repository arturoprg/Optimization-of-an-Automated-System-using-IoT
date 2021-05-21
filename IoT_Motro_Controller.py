# The code bellow is executed just when the function is initialized
if initialize:
    # Initialize outputs
    L1_current = [0.0, 0.0, 0.0]
    L2_current = [0.0, 0.0, 0.0]
    L3_current = [0.0, 0.0, 0.0]
    T1_voltage = [0.0, 0.0, 0.0]
    T2_voltage = [0.0, 0.0, 0.0]
    T3_voltage = [0.0, 0.0, 0.0]
    n_current = 1.96
    actuator_state = 0
    setup_data = "{}"
    actuator_value = "10"
else:
   # Check input voltage
  in_voltage_ok = 20<(x1_voltage[0]-x2_voltage[0])<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    on = 0.1
    value = 0.1
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
            actuator_value = update_output_json[topic]
        
  # Driver Error
  elif actuator_state == 4:
    enable_driver = False
    
    
  ctrl = int(actuator_value)
  T1_voltage = [L1_voltage[0],L1_voltage[1]*ctrl/10,L1_voltage[2]]
  T2_voltage = [L1_voltage[0],L2_voltage[1]*ctrl/10,L2_voltage[2]]
  T3_voltage = [L1_voltage[0],L3_voltage[1]*ctrl/10,L3_voltage[2]]
  L1_current = T1_current
  L2_current = T2_current
  L3_current = T3_current