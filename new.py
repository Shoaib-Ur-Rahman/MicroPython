from machine import Pin
print("ESP32 is running!")
print(Pin(4, Pin.IN, Pin.PULL_UP).value())