# The code bellow is executed just when the function is initialized
if initialize:
  # Initialize outputs
  signal_voltage = [0, 0, 0]
  l1_out_voltage = [0.0, 0.0, 0.0]
  l2_out_voltage = [0.0, 0.0, 0.0]
  l3_out_voltage = [0.0, 0.0, 0.0]
  l1_in_current = [0.0, 0.0, 0.0]
  l2_in_current = [0.0, 0.0, 0.0]
  l3_in_current = [0.0, 0.0, 0.0]
  switch_pos = [0.06, 0.0, -0.0058, 0.0, -0.4226, 0.0, 0.9063]
  
  overload = False
  switch_pressed_last = False
  sensor_state = 0
  setup_data = "{}"
  update_input = "{}"

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
      # Handle switch_pressed event
      if switch_pressed != switch_pressed_last:
        if switch_pressed:
          overload = not overload
      switch_pressed_last = switch_pressed
    
      # Check which state we are in
      if not overload:
        # Check if any current exceeds max_current
        if (l1_out_current[0] > max_current or
           l2_out_current[0] > max_current or
           l3_out_current[0] > max_current):
            overload = True
        else:
            switch_pos[4] = -0.4226
            # Close all connections
            l1_out_voltage = l1_in_voltage
            l2_out_voltage = l2_in_voltage
            l3_out_voltage = l3_in_voltage
            l1_in_current = l1_out_current
            l2_in_current = l2_out_current
            l3_in_current = l3_out_current
            send_value = "TRUE"
            
      if overload:
        switch_pos[4] = 0.4226
        # Open all connections
        l1_out_voltage = [0.0, 0.0, 0.0]
        l2_out_voltage = [0.0, 0.0, 0.0]
        l3_out_voltage = [0.0, 0.0, 0.0]
        l1_in_current = [0.0, 0.0, 0.0]
        l2_in_current = [0.0, 0.0, 0.0]
        l3_in_current = [0.0, 0.0, 0.0]
        send_value = "FALSE"
        
      # Send data to the driver
      update_input = json.dumps({topic: send_value})

  # Driver Error
  elif sensor_state == 4:
    enable_driver = False
    
#Component behavior
  # Handle switch_pressed event
  if switch_pressed != switch_pressed_last:
    if switch_pressed:
      overload = not overload
  switch_pressed_last = switch_pressed
    
  # Check which state we are in
  if not overload:
    # Check if any current exceeds max_current
    if (l1_out_current[0] > max_current or
       l2_out_current[0] > max_current or
       l3_out_current[0] > max_current):
      overload = True
    else:
      switch_pos[4] = -0.4226
      # Close all connections
      l1_out_voltage = l1_in_voltage
      l2_out_voltage = l2_in_voltage
      l3_out_voltage = l3_in_voltage
      l1_in_current = l1_out_current
      l2_in_current = l2_out_current
      l3_in_current = l3_out_current
            
  if overload:
    switch_pos[4] = 0.4226
    # Open all connections
    l1_out_voltage = [0.0, 0.0, 0.0]
    l2_out_voltage = [0.0, 0.0, 0.0]
    l3_out_voltage = [0.0, 0.0, 0.0]
    l1_in_current = [0.0, 0.0, 0.0]
    l2_in_current = [0.0, 0.0, 0.0]
    l3_in_current = [0.0, 0.0, 0.0]
