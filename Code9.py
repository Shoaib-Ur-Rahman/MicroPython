from machine import Pin,ADC
from time import sleep
led=Pin(4,Pin.OUT)
button_mode=Pin(18,Pin.IN,Pin.PULL_UP)
button_manual=Pin(19,Pin.IN,Pin.PULL_UP)
ldr=ADC(Pin(34))
ldr.init(atten=ADC.ATTN_11DB)
button_pressed_flag=False
def button_irq(pin):
    global button_pressed_flag
    button_pressed_flag=True
button_mode.irq(trigger=Pin.IRQ_FALLING, handler=button_irq)
led_state=0
auto_mode=False
threshold=64000
previous=1
while True:
    current=button_manual.value()
    reading=ldr.read_u16()
    if button_pressed_flag:
        button_pressed_flag=False
        auto_mode=not auto_mode
    if auto_mode:
        if reading<threshold:
            led.value(0)
        else:
            led.value(1)
    else:
        if current==0 and previous==1:
            sleep(0.01)
            if button_manual.value()==0:
                led_state=not led_state
                led.value(led_state)
    previous=current
    sleep(0.01)