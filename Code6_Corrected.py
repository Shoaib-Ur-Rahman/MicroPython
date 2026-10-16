from machine import ADC, Pin

adc = ADC(Pin(34))

print("ADC object:", adc)
print("Has init:", hasattr(adc, "init"))
print("Has atten:", hasattr(adc, "atten"))
print("Has read_u16:", hasattr(adc, "read_u16"))
print("Has read:", hasattr(adc, "read"))