# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  selected_color = [0.3, 0.3, 0.3, 1]
  button_frame = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"
  maintained = False
  actuator_value = "False"
  selected_color = color_off

# The code bellow is executed each execution step with the updated dt
else:
   # Check input voltage
  in_voltage_ok = 15<(x1_voltage[0]-x2_voltage[0])<30
  # Device powered off, Reset sensor_state
  if not in_voltage_ok:
    selected_color = color_off
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
        topicPub: {'datatype': 'str', 'size': 1, 'operation': 'write'},
        topicSub: {'datatype': 'str', 'size': 1, 'operation': 'read'},
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
      # Light
      update_output_json = json.loads(update_output)
      if topicSub in update_output_json:
        actuator_value = update_output_json[topicSub]
        
      if actuator_value == "On":
        selected_color = color_on
      else:
        selected_color = color_off
          
      if sensor_value:
        send_value = "TRUE"
      else:
        send_value = "FALSE"
      # Send data to the driver
      update_input = json.dumps({topicPub: send_value})


  # Driver Error
  elif sensor_state == 4:
    enable_driver = False
    
# Component behavior
  # Button
  if button_maintained:	# maintained buttons
    if pressed:
      maintained = not maintained
        
    if maintained:
      button_frame[0] =  -0.005
      sensor_value = button_NO
    else:
      button_frame[0] = 0.0
      sensor_value = not button_NO
        
  else:			# not maintained buttons
    if pressed:
      button_frame[0] =  -0.005
      sensor_value = button_NO
    else:
      button_frame[0] = 0.0
      sensor_value = not button_NO