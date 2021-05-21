if initialize:
  A2_current = [0.0, 0.0, 0.0]
  A1_current = [0.0, 0.0, 0.0]
  x12_voltage = [0.0, 0.0, 0.0]
  x11_current = [0.0, 0.0, 0.0]
  x14_voltage = [0.0, 0.0, 0.0]
  x13_current = [0.0, 0.0, 0.0]
  state = 0
  setup_data = "{}"
  actuator_value = "Off"

else:

  if state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    update_input = "{}"
    sensor_value = "FALSE"
    state = 1
    step_time = 0.1
  
  elif state == 1:
    setup_dict = {
      'parameters': {
        'ip': ip_address,
        'force_write':0
      },
      'variables': {
        topic: {'datatype': 'str', 'size': 1, 'operation': 'write'},
      }
    }
    setup_data = json.dumps(setup_dict)
    state = 2
  
  elif state == 2:
    enable_driver = True
    if driver_status == 'RUNNING':
      state = 3
      
  elif state == 3:
    step_time = 0
    if driver_status != 'RUNNING':
      state = 4
  
    if (A1_voltage[0] - A2_voltage[0]) > 20:
      A1_current = [0.01, 0.0, 0.0]
      A2_current = [-0.01, 0.0, 0.0]
      x12_voltage = x11_voltage
      x11_current = x12_current
      x14_voltage = x13_voltage
      x13_current = x14_current
      sensor_value = "TRUE"
    else:
      A1_current = [0.0, 0.0, 0.0] 
      A2_current = [0.0, 0.0, 0.0]
      x12_voltage = [0.0, 0.0, 0.0]
      x11_current = [0.0, 0.0, 0.0]
      x14_voltage = [0.0, 0.0, 0.0]
      x13_current = [0.0, 0.0, 0.0]
      sensor_value = "FALSE"
    
  elif sensor_state == 4:
    enable_driver = False