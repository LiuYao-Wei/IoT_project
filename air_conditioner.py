import machine
import time
import network, time
_station = network.WLAN(network.STA_IF)
_station.active(True)
_station.connect("Dustin", "a12345678")
print('Connecting to network...')
while _station.isconnected() == False:
    time.sleep(1)
    print('.', end="")
else:
    print(_station.ifconfig())
    print("成功連線!!")
from umqttsimple import MQTTClient
client = MQTTClient(client_id="I4B01", server="broker.emqx.io", port=1883, user="", password="", keepalive=120)
client.connect(False)
print("Connect to broker")
import dht
gpioPin = dht.DHT22(machine.Pin(14))
middle_Led = machine.Pin(11, machine.Pin.OUT, value=0)
Left_Led = machine.Pin(15, machine.Pin.OUT, value=0)
Right_Led = machine.Pin(16, machine.Pin.OUT, value=0)
def sub_cb(topic,msg):
    print("topic=",topic,"msg=",msg)
    if (msg == b"ON"):
        gpioPin.measure()
        temp = round(gpioPin.temperature(), 1)
        humi = round(gpioPin.humidity(), 1)
        print(temp)
        if (temp > 24.5):
            Right_Led.value(1)
        elif (temp <= 24.5):
            Left_Led.value(1)
        time.sleep(5)
        while True:
            gpioPin.measure()
            temp = round(gpioPin.temperature(), 1)
            humi = round(gpioPin.humidity(), 1)
            print(temp)
            if (temp > 24.5):
                Right_Led.value(1)
                Left_Led.value(0)
            elif (temp <= 24.5):
                Left_Led.value(1)
                Right_Led.value(0)
            time.sleep(2)
client.set_callback(sub_cb)
pingCounter = 0
def timerCheckMsg_callback(timer):
    global pingCounter
    try:    
        client.check_msg()
        if pingCounter >= 300:
            client.ping()
            pingCounter = 0
        else:
            pingCounter += 1
    except OSError as e:
        print("reconnecting...")
        client.connect(False)
        print("reconnected.")
timerCheckMsg = machine.Timer()
timerCheckMsg.init(period=400, mode=machine.Timer.PERIODIC, callback=timerCheckMsg_callback)

client.subscribe(topic="I4B01", qos=0)