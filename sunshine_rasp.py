import paho.mqtt.client as mqtt
import time
from threading import Thread, Lock
from ccs811 import *
from hdc2010 import *

mutex = Lock()
broker_address="broker.hivemq.com"
port = 1883

## Default Measurements Frequency (seconds) ##
measFreqTemp = 10
measFreqHum = 20
measFreqTvoc = 30
measFreqCo2 = 40

## COMMON FOR MQTT ##
def onMessage(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    topicVariableMapper(message.topic, str(message.payload.decode("utf-8")))
    printCurrentFreqs()

def onConnect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("rasp3BFreqTemp") 
    client.subscribe("rasp3BFreqHum") 
    client.subscribe("rasp3BFreqTvoc") 
    client.subscribe("rasp3BFreqCo2") 
    client.subscribe("microcontrollerInit")

def onLog(client, userdata, level, buf):
    print("log: ",buf)

## LOGIC ##
def printCurrentFreqs(): 
    global measFreqTemp
    global measFreqHum  
    global measFreqTvoc
    global measFreqCo2
    print("Current measFreqTemp", measFreqTemp)
    print("Current measFreqHum", measFreqHum)
    print("Current measFreqTvoc", measFreqTvoc)
    print("Current measFreqCo2", measFreqCo2)

def topicVariableMapper(topic, value):
    mutex.acquire()
    global measFreqTemp
    global measFreqHum
    global measFreqTvoc
    global measFreqCo2
    print("Receive data with Topic=", topic)
    try:
        if topic == "rasp3BFreqTemp":
            print(value)
            measFreqTemp = int(value)
        elif topic == "rasp3BFreqHum":
            print(value)
            measFreqHum = int(value)
        elif topic == "rasp3BFreqTvoc":
            print(value)
            measFreqTvoc = int(value)
        elif topic == "rasp3BFreqCo2":
            measFreqCo2 = int(value)
            print(value)
        elif topic == "microcontrollerInit":
            client.publish("rasp3BFreqTemp", measFreqTemp)
            client.publish("rasp3BFreqHum", measFreqHum)
            client.publish("rasp3BFreqTvoc", measFreqTvoc)
            client.publish("rasp3BFreqCo2", measFreqCo2)
        else:
            print("Invalid topic")
    finally:
        mutex.release()

def sendTemperature():
    while True:
        temp = hdc2010ReadTemp()
        if temp > 0:
            client.publish("rasp3BTemperature", temp)

        mutex.acquire()
        try:
            global measFreqTemp
            measFreqTempLocal = measFreqTemp
        finally:
            mutex.release()

        print("function ~~ SendTemperature()", measFreqTempLocal) # debug
        time.sleep(measFreqTempLocal)

def sendHumidity():
    while True:
        hum = hdc2010ReadHumidity()
        if hum > 0:
            client.publish("rasp3BHumidity", hum)

        mutex.acquire()
        try:
            global measFreqHum
            measFreqHumLocal = measFreqHum
        finally:
            mutex.release()

        print("function ~~ sendHumidity()", measFreqHumLocal) # debug
        time.sleep(measFreqHumLocal)

def sendTvoc():
    while True:
        if ccs811CheckDataAndUpdate():
            tvoc = ccs811GetTVOC()
            if tvoc > 0 and tvoc < 1187:
                client.publish("rasp3BTvoc", tvoc)
        elif ccs811CheckForError():
            ccs811PrintError()

        mutex.acquire()
        try:
            global measFreqTvoc
            measFreqTvocLocal = measFreqTvoc
        finally:
            mutex.release()

        print("function ~~ sendTvoc()", measFreqTvocLocal) # debug
        time.sleep(measFreqTvocLocal)

def sendCo2():
    while True:
        if ccs811CheckDataAndUpdate():
            co2 = ccs811GetCO2()
            if co2 > 0 and co2 < 8192:
                client.publish("rasp3BCo2", co2)
        elif ccs811CheckForError():
            ccs811PrintError()

        mutex.acquire()
        try:
            global measFreqCo2
            measFreqCo2Local = measFreqCo2
        finally:
            mutex.release()

        print("function ~~ sendCo2()", measFreqCo2Local) # debug
        time.sleep(measFreqCo2Local)

## SENSOR INIT ##
ccs811Begin(CCS811_driveMode_1sec)                              #start CCS811, data update rate at 1sec
hdc2010Reset()                                                  #start with sensor reset
hdc2010SetMeasurementsMode(HDC2010_TEMP_AND_HUMID)              #Set measurements to temperature and humidity 14bits resolution
hdc2010SetRate(HDC2010_ONE_HZ)                                  #Set measurement frequency to 1 Hz
hdc2010SetTempRes(HDC2010_NINE_BIT)                         #Set temperature resolution at 14bits
hdc2010SetHumidRes(HDC2010_NINE_BIT)                        #Set humidity resolution at 14bits
hdc2010TriggerMeasurement()                                     #trigger measurements
sleep(1)

## MQTT INIT ##
printCurrentFreqs()
print("creating new client Raspberry3B")
client = mqtt.Client("Raspberry3B")
client.on_message=onMessage
client.on_log=onLog
client.on_connect=onConnect
print("connecting to broker")
client.connect(broker_address, port)
client.loop_start()

## THREADS INIT ##
tempSenderThread = Thread(target=sendTemperature)
humSenderThread = Thread(target=sendHumidity)
tvocSenderThread = Thread(target=sendTvoc)
co2SenderThread = Thread(target=sendCo2)

tempSenderThread.daemon = True
humSenderThread.daemon = True
tvocSenderThread.daemon = True
co2SenderThread.daemon = True

tempSenderThread.start()
humSenderThread.start()
tvocSenderThread.start()
co2SenderThread.start()

while True:
    pass
