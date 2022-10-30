import time
import machine # ---- 添加 --------
import network
from umqttsimple import MQTTClient
import socket
import network
import camera
import ujson
import control

lightvalue = 55
speedvalue = 50
machine.freq(240000000)
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('FEN_2.4G', '25575566')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())

def forward():
    print("forward")
    for i in range (5):
        led_pin.value(1)
        time.sleep(0.1)
        led_pin.value(0)
        time.sleep(0.1)

def sub_cb(topic, msg): # 回调函数，收到服务器消息后会调用这个函数
    print(topic, msg)
    global lightvalue
    global speedvalue
    if topic.decode("utf-8") == "carctl":
        try:
            setvalue = ujson.loads(msg)
            # print(setvalue)
            if "lightvalue" in setvalue:
                lightvalue = setvalue["lightvalue"]
                print(lightvalue,"bbb")
                control.led(lightvalue)
            elif  "speedvalue" in setvalue:
                speedvalue = setvalue["speedvalue"]
                print(speedvalue,"aaa")
        except:
            pass
        
        if msg.decode("utf-8") == "forward":
            control.forward(speedvalue)
        elif msg.decode("utf-8") == "back":
            control.back(speedvalue)
        elif msg.decode("utf-8") == "left":
            control.left(speedvalue)
        elif msg.decode("utf-8") == "right":
            control.right(speedvalue)
        elif msg.decode("utf-8") == "stop":
            control.stop()
        elif msg.decode("utf-8") == "paysuccess":
            control.paysuccess()
            
        
#         try:
#             lightvalue = setvalue["lightvalue"]
#             print(lightvalue)
#             speedvalue = setvalue["speedvalve"]
#             print(speedvalue,"aaa")
#             print(lightvalue,"bbb")
# 
#         except:
#         
#             pass
#     if msg.decode("utf-8") == "forward":
#         print("forward")
        
    # ---- 添加 --------
#     if topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "on":
#         led_pin.value(1)
#         print("techfens")
#     elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "off":
#         led_pin.value(0)
#     elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "flash":
#         for i in range (5):
#             led_pin.value(1)
#             time.sleep(0.1)
#             led_pin.value(0)
#             time.sleep(0.1)
#     elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "stop":
#         led_pin.value(0)
#     elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "back":
#         led_pin.value(1)
#     elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "aaa":
#         led2 = PWM(Pin(4))
#         led2.freq(1000)
# 
#         while True:
#             for i in range(0, 1024):
#                 led2.duty(i)
#                 time.sleep_ms(1)
#                 
#             for i in range(1023, -1, -1):
#                 led2.duty(i)
#                 time.sleep_ms(1)
#                 
#     elif topic.decode("utf-8") == "ledctl"


    # ---- 添加 --------

def connect():
    # 1. 联网
    do_connect()

    # 2. 创建mqt
    c = MQTTClient("my_esp32cam", "150.158.214.32")  # 建立一个MQTT客户端
    c.set_callback(sub_cb)  # 设置回调函数
    c.connect()  # 建立连接
    c.subscribe(b"carctl")  # 监控ledctl这个通道，接收控制命令
    return c

# c.subscribe(b"carctl")
c = connect()
# ---- 添加 --------
# 3. 创建LED对应Pin对象
# led_pin = Pin(4, Pin.OUT)
# ---- 添加 --------

try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)


# 其他设置：
# 上翻下翻
camera.flip(0)
#左/右
camera.mirror(1)

# 分辨率
camera.framesize(camera.FRAME_HVGA)
# 选项如下：
# FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
# FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
# FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
# FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
# FRAME_P_FHD FRAME_QSXGA
# 有关详细信息，请查看此链接：https://bit.ly/2YOzizz

# 特效
camera.speffect(camera.EFFECT_NONE)
#选项如下：
# 效果\无（默认）效果\负效果\ BW效果\红色效果\绿色效果\蓝色效果\复古效果
# EFFECT_NONE (default) EFFECT_NEG \EFFECT_BW\ EFFECT_RED\ EFFECT_GREEN\ EFFECT_BLUE\ EFFECT_RETRO

# 白平衡
camera.whitebalance(camera.WB_HOME)
#选项如下：
# WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

# 饱和
camera.saturation(0)
#-2,2（默认为0）. -2灰度
# -2,2 (default 0). -2 grayscale 

# 亮度
camera.brightness(0)
#-2,2（默认为0）. 2亮度
# -2,2 (default 0). 2 brightness

# 对比度
camera.contrast(0)
#-2,2（默认为0）.2高对比度
#-2,2 (default 0). 2 highcontrast

# 质量
camera.quality(10)
#10-63数字越小质量越高

# socket UDP 的创建
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
def main():
#     try:
    i = 0
    n = 0
    while True:
        c.check_msg()
        buf = camera.capture()  # 获取图像数据
        s.sendto(buf, ("150.158.214.32", 5904))  # 向服务器发送图像数据
        i += 1
        if i >= 30:
            if c.ping() is None:
                n += 1
                #print("alive", n)
                i = 0
        
            # time.sleep(0.1)
    #         isconnet = mqtt.ping()
    #         print(isconnet)
    #         time.sleep(0.5)
#     except OSError as e:
#         print('Failed to connect to MQTT broker. Reconnecting...')
#         time.sleep(1)
#         do_connect()
#     finally:
#             camera.deinit()
    

try:
    main()
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(1)
    machine.reset()
    do_connect()
#     time.sleep(5)
    main()
finally:
    camera.deinit()
    
