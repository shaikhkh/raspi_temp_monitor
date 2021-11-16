#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys
import paho.mqtt.client as paho
from threading import Thread, Lock
broker="localhost"
port=1883

log_path = '/home/pi/temp_sensor/logs/';

sensor_paths = ['/sys/bus/w1/devices/28-03213151049a/w1_slave',
'/sys/bus/w1/devices/28-03213175b650/w1_slave',
'/sys/bus/w1/devices/28-0321317bf89e/w1_slave',
'/sys/bus/w1/devices/28-0321317c502a/w1_slave',
'/sys/bus/w1/devices/28-0321317c91b6/w1_slave',
'/sys/bus/w1/devices/28-0321317d7f8b/w1_slave',
'/sys/bus/w1/devices/28-0321317e4a48/w1_slave',
'/sys/bus/w1/devices/28-0321317f46e5/w1_slave'];

stop_threads = False;
temp_val_0 = '';
temp_val_1 = '';
temp_val_2 = '';
temp_val_3 = '';
temp_val_4 = '';
temp_val_5 = '';
temp_val_6 = '';
temp_val_7 = '';
temp_threads = [0]*8;

mutex0 = Lock();
mutex1 = Lock();
mutex2 = Lock();
mutex3 = Lock();
mutex4 = Lock();
mutex5 = Lock();
mutex6 = Lock();
mutex7 = Lock();

def on_publish(client,userdata,result):
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT server");
    else:
        print(f"Connected fail with code {rc}");

def readTemp(sensorName) :
    try:
      f = open(sensorName, 'r')
      lines = f.read()
      f.close()
      if "YES" in lines:
          (discard, sep, tempData) = lines.partition(' t=')
          tempCelsius = float(tempData) / 1000.0
          tempKelvin = 273 + float(tempData) / 1000
          tempFahrenheit = float(tempData) / 1000 * 9.0 / 5.0 + 32.0
          return [tempCelsius, tempKelvin, tempFahrenheit]
      else:
          return [0,0,0]
    except IOError:
      print ("Sensor " + sensorName + " not found\n");
      return 0;

def read_temperatures(sensorId):
    while True:
      if stop_threads:
          break;
      if sensorId == 0:
        mutex0.acquire()
        global temp_val_0;
        temp_val_0 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_0);
        mutex0.release()
      elif sensorId == 1:
        mutex1.acquire()
        global temp_val_1;
        temp_val_1 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_1);
        mutex1.release()
      elif sensorId == 2:
        mutex2.acquire()
        global temp_val_2;
        temp_val_2 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_2);
        mutex2.release()
      elif sensorId == 3:
        mutex3.acquire()
        global temp_val_3;
        temp_val_3 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_3);
        mutex3.release()
      elif sensorId == 4:
        mutex4.acquire()
        global temp_val_4;
        temp_val_4 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_4);
        mutex4.release()
      elif sensorId == 5:
        mutex5.acquire()
        global temp_val_5;
        temp_val_5 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_5);
        mutex5.release()
      elif sensorId == 6:
        mutex6.acquire()
        global temp_val_6;
        temp_val_6 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_6);
        mutex6.release()
      elif sensorId == 7:
        mutex7.acquire()
        global temp_val_7;
        temp_val_7 = str(readTemp(sensor_paths[sensorId])[0]);
        #print("from thread "+str(sensorId)+":"+temp_val_7);
        mutex7.release()
      else:
        break;
      time.sleep(1)

try:
    file_name = log_path+"temp_log_"+time.strftime('%Y%m%d_%H%M%S'+".csv");
    print("Logging to file : " + file_name);
    client1= paho.Client("control1");
    client1.on_publish = on_publish;
    client1.on_connect = on_connect;
    client1.connect(broker,port);
    time.sleep(10);
    for i in range(8):
      temp_threads[i] = Thread(target = read_temperatures, args = (i, ));
      temp_threads[i].start();
    with open(file_name, "a") as log:
      log.write("timestamp,temp_sensor_1,temp_sensor_2,temp_sensor_3,temp_sensor_4,temp_sensor_5,temp_sensor_6,temp_sensor_7,temp_sensor_8\n");
      while True :
          current_time = str(int(time.time()*1000));
          mutex0.acquire()
          mutex1.acquire()
          mutex2.acquire()
          mutex3.acquire()
          mutex4.acquire()
          mutex5.acquire()
          mutex6.acquire()
          mutex7.acquire()
          write_buf = str(current_time+","+temp_val_0+","+temp_val_1+","+temp_val_2+","+temp_val_3+","+temp_val_4+","+temp_val_5+","+temp_val_6+","+temp_val_7+"\n");
          mutex0.release()
          mutex1.release()
          mutex2.release()
          mutex3.release()
          mutex4.release()
          mutex5.release()
          mutex6.release()
          mutex7.release()
          print(write_buf);
          log.write(write_buf);
          log.flush();
          ret= client1.publish("sensor/1",temp_val_0);
          ret= client1.publish("sensor/2",temp_val_1);
          ret= client1.publish("sensor/3",temp_val_2);
          ret= client1.publish("sensor/4",temp_val_3);
          ret= client1.publish("sensor/5",temp_val_4);
          ret= client1.publish("sensor/6",temp_val_5);
          ret= client1.publish("sensor/7",temp_val_6);
          ret= client1.publish("sensor/8",temp_val_7);
          time.sleep(2)
except KeyboardInterrupt:
    print('Exit program');
    stop_threads = True;
except Exception as e:
    print(str(e))
    stop_threads = True;
    sys.exit(1)
finally:
    stop_threads = True;
    sys.exit(0)
