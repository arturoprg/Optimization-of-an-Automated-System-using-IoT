# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  A2_current = [0.0, 0.0, 0.0]
  A1_current = [0.0, 0.0, 0.0]
  x11_current = [0.0, 0.0, 0.0]
  x12_voltage = [0.0, 0.0, 0.0]
  x14_voltage = [0.0, 0.0, 0.0]
  state = 0
  setup_data = "{}"
  actuator_value = "Off"
# The code bellow is executed each execution step with the updated dt
else:
  # Actuator powered off
  if state == 0:
    # Reset driver
    enable_driver = False
    setup_data = "{}"
    step_time = 0 
    state = 1
    step_time = 0.1
            
  # Power up and Setup driver connection
  elif state == 1:
    if not send_or_receive:
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
    else:
       setup_dict = {
        'parameters': {
          'ip':ip_address
        },
        'variables': {
          topic: {'datatype': 'str', 'size': 1, 'operation': 'read'},
        }
      }
    setup_data = json.dumps(setup_dict)
    state = 2
            
  # Driver connecting
  elif state == 2:
    # Enable driver, wait for response
    enable_driver = True
    if driver_status == 'RUNNING':
      state = 3
            	
  # Driver ready and running
  elif state == 3:
    # Error if connection lost
    step_time = 0
    if driver_status != 'RUNNING':
        state = 4
    if send_or_receive == False:
      if (A1_voltage[0] - A2_voltage[0]) > 20:
        A1_current = [0.01, 0.0, 0.0]
        A2_current = [-0.01, 0.0, 0.0]
        # Connect 11 and 14
        x14_voltage = x11_voltage
        x11_current = x14_current
        # Disconnect x12
        x12_voltage = [0.0, 0.0, 0.0]
        send_value = "TRUE"
      else:
        A1_current = [0.0, 0.0, 0.0] 
        A2_current = [0.0, 0.0, 0.0]
        # Connect 11 and 12
        x12_voltage = x11_voltage
        x11_current = x12_current
        # Disconnect x14
        x14_voltage = [0.0, 0.0, 0.0]
        send_value = "FALSE"
      update_input = json.dumps({topic: send_value})
    else:
      update_output_json = json.loads(update_output)
      if topic in update_output_json:
        actuator_value = update_output_json[topic]
      if actuator_value == "True":
        A1_current = [0.01, 0.0, 0.0]
        A2_current = [-0.01, 0.0, 0.0]
        # Connect 11 and 14
        x14_voltage = x11_voltage
        x11_current = x14_current
        # Disconnect x12
        x12_voltage = [0.0, 0.0, 0.0]
      else:
        A1_current = [0.0, 0.0, 0.0] 
        A2_current = [0.0, 0.0, 0.0]
        # Connect 11 and 12
        x12_voltage = x11_voltage
        x11_current = x12_current
        # Disconnect x14
        x14_voltage = [0.0, 0.0, 0.0]    
        
  elif state == 4:
    enable_driver = False