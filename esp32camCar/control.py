from machine import Pin, PWM
import time

IO12_INT1 = Pin(12, mode=Pin.OUT)
IO13_INT2 = Pin(13, mode=Pin.OUT)
IO14_INT3 = Pin(14, mode=Pin.OUT)
IO15_INT4 = Pin(15, mode=Pin.OUT)
IO02_PWM1 = Pin(2, mode=Pin.OUT)
IO02_PWM1 = PWM(IO02_PWM1, 78125)

IO12_INT1.value(0)
IO13_INT2.value(0)
IO14_INT3.value(0)
IO15_INT4.value(0)

led_pwm = PWM(Pin(4))
led_pwm.freq(78125)



def led(lightvalue):
    print("forward_def")
    led_pwm.duty(lightvalue*10)

def forward(speedvalue):
    print("forward",speedvalue)
    IO02_PWM1.duty(500+speedvalue*5)
    IO12_INT1.value(0)
    IO13_INT2.value(1)
    IO14_INT3.value(0)
    IO15_INT4.value(1)


def back(speedvalue):
    print("back",speedvalue)
    IO02_PWM1.duty(500+speedvalue*5)
    IO12_INT1.value(1)
    IO13_INT2.value(0)
    IO14_INT3.value(1)
    IO15_INT4.value(0)

    
def left(speedvalue):
    print("left",speedvalue)
    IO02_PWM1.duty(600+speedvalue)
    IO12_INT1.value(0)
    IO13_INT2.value(1)
    IO14_INT3.value(1)
    IO15_INT4.value(0)


def right(speedvalue):
    print("right",speedvalue)
    IO02_PWM1.duty(600+speedvalue)
    IO12_INT1.value(1)
    IO13_INT2.value(0)
    IO14_INT3.value(0)
    IO15_INT4.value(1)

    
def stop():
    print("stop")
    IO12_INT1.value(0)
    IO13_INT2.value(0)
    IO14_INT3.value(0)
    IO15_INT4.value(0)

    # IO02_PWM1.duty(0)
    
def paysuccess():
    print("pay success")
    
    


# while True:
#     IO02_PWM1.duty(1000)
#     IO12_INT1.value(1)
#     IO13_INT2.value(0)
#     print("OK")
#     time.sleep(2)
#     IO02_PWM1.duty(800)
#     time.sleep(2)
    
# IO12_INT1 = PWM(Pin(12))
# IO12_INT1.freq(78125)
# IO12_INT1.duty(0)
# 
# IO13_INT2 = PWM(Pin(13))
# IO13_INT2.freq(78125)
# IO13_INT2.duty(1023)




# LMotor1 = PWM(Pin(13))
# LMotor1.freq(78125)
# LMotor1.duty()
# 
# LMotor2 = PWM(Pin(12))
# LMotor1.freq(78125)

# RMotor1 = PWM(Pin(14))
# RMotor1.freq(78125)
# 
# RMotor2 = PWM(Pin(15))
# RMotor2.freq(78125)

# 
# while True:
#     for i in range(0, 1024):
#         led2.duty(i)
#         time.sleep_ms(1)
#         
#     for i in range(1023, -1, -1):
#         led2.duty(i)
#         time.sleep_ms(1)
