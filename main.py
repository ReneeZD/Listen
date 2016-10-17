import gc,ure,time
from machine import Pin, I2C, RTC

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)

        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def display(command):


    if command=="time":
        x.fill(0)
        a = rtc.datetime()
        x.text(str(a[4]) + ':' + str(a[5]) + ':' + str(a[6]), 1, 1)
        x.show()
    if command=="off":
        x.fill(0)
        x.show()
    if (command!="time") & (command!="off"):
        x.fill(0)
        x.text(command,1,1)
        x.show()



rtc = RTC()
rtc.datetime((2016,12,30,4,1,1,1,1))
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
import ssd1306

x = ssd1306.SSD1306_I2C(128, 32, i2c)
# flag = 0

do_connect()
import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
s.settimeout(0.1)
command="off";
print('listening on', addr)

while True:

    try:
        cl,_ = s.accept()
        cl.setblocking(False)
        print('client connected from', addr)
        while True:
            line = cl.read()
            if line!=None:
                break
        temp1 = ure.search('"key":"(.*)"}', line)
        command=temp1.group(1)
        # if command=="time":
        #     flag=1
        # if command=="off":
        #     flag=0
        response = b'HTTP/1.0 200 OK\r\nServer: esp8266\r\nContent-Type: application/json\r\nContent-Length: 0\r\nConnection: Closed\r\n\r\n '
        cl.send(response)
        cl.close()

    except:
        display(command)

    finally:
        pass


