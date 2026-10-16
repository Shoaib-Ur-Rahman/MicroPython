import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Wi-Fi active:", wlan.active())

for i in range(6):
    print("Wi-Fi status:", wlan.status())
    time.sleep(5)