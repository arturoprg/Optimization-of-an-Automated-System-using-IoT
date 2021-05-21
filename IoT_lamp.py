# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  bulb_color = [0.1, 0.1, 0.1, 1.0]
  actuator_state = 0
  setup_data = "{}"
  actuator_value = "Off"
  n_current = 0.054*6  # 9W
  Phi = 45.57		# cos(phi) = 0.7
# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 220<(x1_voltage[0]-x2_voltage[0])<240
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    on = 0.1
    value = 0.1
    x1_current = [0,0,0]
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
        #topic_lastwill: {'datatype': 'str', 'size': 1, 'operation': 'write'},
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
        
        try:
            if (0 < float(actuator_value) and 10 >= float(actuator_value)):
                value = (10-float(actuator_value))/10
                on = 1
                x1_current = [n_current/value,50,x1_voltage[2]-Phi]
            else:
                value = 0.1
                on = 0.1  
                x1_current = [0,0,0]
        except:
            if actuator_value == "On":
                on = 1
                value = 0
                x1_current = [n_current,50,x1_voltage[2]-Phi]
            elif actuator_value == "Off":
                on = 0.1
                value = 0.1
                x1_current = [0,0,0]
        x2_current = [-x1_current[0],x1_current[1],x1_current[2]]

  # Driver Error
  elif actuator_state == 4:
    enable_driver = False
    
  x2_current = [-x1_current[0],x1_current[1],x1_current[2]]
  bulb_color = [on, on, value, 1.0]