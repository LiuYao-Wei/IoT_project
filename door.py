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
    
import time
from hc_sr04 import HCSR04
sensor1 = HCSR04(trigger_pin=12, echo_pin=13, echo_timeout_us=1000000)
LED = machine.Pin(11, machine.Pin.OUT, value=0)
btndoor = machine.Pin(19, machine.Pin.IN,machine.Pin.PULL_UP)
adcPin = machine.ADC(machine.Pin(26))
import dht
dhtSensor = dht.DHT22(machine.Pin(14))
while True:
    distance = round(sensor1.distance_cm(), 1)
    print("d=",distance)
    if (distance < 10):
        print("有人")
        LED.value(1)
        print("已開啟電燈")
        while True:
            isopen=btndoor.value()
            print(isopen)
            if (isopen == 0):
                break
            time.sleep(1)
        from umqttsimple import MQTTClient
        client = MQTTClient(client_id="id001", server="broker.emqx.io", port=1883, user="", password="", keepalive=120)
        client.connect(False)
        client.publish(topic="I4B01", msg=str("ON"), qos=0, retain=False)
        print("以傳送")
        while True:
            light = adcPin.read_u16()
            print("light = ",light)
            if (light > 10000):
                LED.value(0)
                print("已關閉電燈")
                break
            time.sleep(1)
    time.sleep(1)