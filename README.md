# raspi_temp_monitor
This project is used to connect 8 DS18B20 (https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) 
temperature sensors on the 1-wire bus with a raspberry pi and then monitor them using node-red.
The project is split in two main source files
1. read_temp.py
  This python script runs on the raspberry pi. I tested this on raspberry pi 3B. 
  The script reads the temperature sensors on the 1-wire bus, logs them to a csv file and 
  also publishes them on the MQTT topics. Each sensor has its own topic.
2. Flows.json
 This is the node red flow file and is used for user interface. This shows the temperature plot and values from all 8 sensors.
 It also gives a file interface option for downloading and viewing the logged csv files on the raspberry pi.
 
 To use in your project, following changes are required
 
 1. Update log_path and sensor_paths in the read_temp.py file
 2. Update "Init" and "Reset" nodes with the path to your log files on the raspberry pi
 
 Credit to "Csongor Varga". I am using the file browser approach from his project, youtube link here -> (https://www.youtube.com/watch?v=3QgK4IAAqcQ&t=148s)
