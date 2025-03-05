import machine
import network, time
_station = network.WLAN(network.STA_IF)
_station.active(True)
_station.connect("david", "qmtx2263")
print('Connecting to network...')
while _station.isconnected() == False:
    time.sleep(1)
    print('.', end="")
else:
    print(_station.ifconfig())
    print("connected")
gpioPinLED = machine.Pin(11, machine.Pin.OUT, value=0)
gpioPinLEDLeft = machine.Pin(15, machine.Pin.OUT, value=0)
gpioPinLEDRight = machine.Pin(16, machine.Pin.OUT, value=0)
buzzer = machine.Pin(18, machine.Pin.OUT, value=0)
distance = 0
ledState = 0
setting = 0
max = 2
min = 0
inc = 1
pl = 1
def led(payload):
    global ledState,setting
    print("=====p0000:",payload)
    if (payload == "0"):
        gpioPinLED.value(0)
        gpioPinLEDLeft.value(0)
        gpioPinLEDRight.value(0)
        ledState = 0
    if (payload == "1"):
        print("=====p1111:",payload,"s=",setting)
        if (str(setting) == "0"):
            gpioPinLED.value(1)
            gpioPinLEDLeft.value(0)
            gpioPinLEDRight.value(0)
        elif (str(setting) == "1"):
            gpioPinLEDLeft.value(1)
            gpioPinLEDRight.value(1)
            gpioPinLED.value(0)
        elif (str(setting) == "2"):
            gpioPinLED.value(1)
            gpioPinLEDLeft.value(1)
            gpioPinLEDRight.value(1)
        ledState = 1
timer1 = machine.Timer()
def timer1_callback(timer):
    global ledState,distance
timer1.init(period=1000, mode=machine.Timer.PERIODIC, callback=timer1_callback)
def start(payload=None):
    global ledState,setting
    print("p:",payload)
    led(payload)
    print("end")
    return ledState

def set(payload=None):
    global ledState,setting
    if (payload == "0"):
        setting = 0
    if (payload == "1"):
        setting = 1
    if (payload == "2"):
        setting = 2
    print("ledst",ledState)
    if (str(ledState) == "1"):
        print("led")
        led("1")
    return setting

import IoT_MQTT
deviceInfo = {"flags": 0x00000001, "classID": 0, "deviceID": 120}
def getTypeID():
    return deviceInfo["deviceID"]
def getFlags():
    return deviceInfo["flags"]
IoT_MQTT.init(server="140.129.6.250", port=8883, user="demo20", password="demo20", ssl=True)
IoT_MQTT.addSensor("/typeID", getTypeID)
IoT_MQTT.addSensor("/flags", getFlags)
IoT_MQTT.addActuator("/122/0/201", start)
def get_1(payload=None):
    return 1
def get_max(payload=None):
    return max
def get_min(payload=None):
    return min
def get_inc(payload=None):
    return inc
IoT_MQTT.addActuator("/122/0/213", set)
IoT_MQTT.addSensor("/122/0/213/desc", get_1)
IoT_MQTT.addSensor("/122/0/213/max", get_max)
IoT_MQTT.addSensor("/122/0/213/min", get_min)
IoT_MQTT.addSensor("/122/0/213/inc", get_inc)
IoT_MQTT.connect()