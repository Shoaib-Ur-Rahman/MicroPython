
import bluetooth
import time

ble = bluetooth.BLE()
devices = {}

def irq(event, data):
    # MicroPython BLE IRQ_SCAN_RESULT = 5
    if event == 5:
        addr_type, addr, adv_type, rssi, adv_data = data
        address = ":".join("%02X" % b for b in addr)
        devices[address] = rssi

        print(
            "BLE device:", address,
            "| RSSI:", rssi,
            "| Advertisement type:", adv_type
        )

try:
    ble.active(True)
    ble.irq(irq)

    print("Scanning for BLE advertisements for 15 seconds...")
    ble.gap_scan(15000, 30000, 30000, True)
    time.sleep_ms(15500)
    ble.gap_scan(None)

    print("\nUnique BLE addresses observed:", len(devices))

    if devices:
        print("PASS: BLE advertisements received")
    else:
        print("INCONCLUSIVE: No advertisements received.")
        print("Try again with an actively advertising BLE device.")

finally:
    try:
        ble.gap_scan(None)
    except Exception:
        pass

    try:
        ble.irq(None)
        ble.active(False)
    except Exception:
        pass

    print("BLE scan stopped; Bluetooth deactivated.")
