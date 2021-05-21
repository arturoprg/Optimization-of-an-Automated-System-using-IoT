# The code below is executed just when the function is initialized
if initialize:
  # Internal variables can be declared here
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"

# The code below is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<x1_voltage[0]-x0_voltage[0]<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    sensor_state = 0
   
  # Sensor powered off
  if sensor_state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    update_input = "{}"
    sensor_value = "FALSE"
    step_time = 0
    
    # Powered on
    if in_voltage_ok:
      sensor_state = 1
      step_time = 0.1
  
  elif sensor_state == 1:
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
    sensor_state = 2
  
  elif sensor_state == 2:
    enable_driver = True
    if driver_status == 'RUNNING':
      sensor_state = 3
      
  elif sensor_state == 3:
    step_time = 0
    if driver_status != 'RUNNING':
      sensor_state = 4
    else:
      if p1_pressure >= p1_trigger_level:
        sensor_value = "TRUE"
      else:
        sensor_value = "FALSE"
      update_input = json.dumps({topic: sensor_value})
      
  elif sensor_state == 4:
    enable_driver = False