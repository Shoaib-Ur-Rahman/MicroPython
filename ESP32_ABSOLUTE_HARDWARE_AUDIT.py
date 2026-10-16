# ESP32_ABSOLUTE_HARDWARE_AUDIT.py
# For classic ESP32 DevKit + MicroPython v1.29.0
# Tests APIs and selected hardware features without external peripherals.
#
# Radio tests:
#   - Wi-Fi scan (receives nearby AP advertisements; does not connect)
#   - BLE scan (receives nearby BLE advertisements)
#   - ESP-NOW init/deinit (does NOT send packets; a second ESP32 is needed
#     for a real peer-to-peer communication test)
#
# Safety:
#   - No flash erase/format.
#   - No Wi-Fi credentials required or stored.
#   - No GPIO is connected to an external load.
#   - Internal temperature reading is RAW, not calibrated Celsius.
#   - The radio tests briefly activate Wi-Fi/BLE and then deactivate them.

import sys
import os
import gc
import time

passed = 0
failed = 0
skipped = 0
missing = 0
attempted = 0


def report(status, name, detail=""):
    global passed, failed, skipped, missing
    print(status + ": " + name)
    if detail:
        print("  " + str(detail))
    if status == "PASS":
        passed += 1
    elif status == "FAIL":
        failed += 1
    elif status == "SKIP":
        skipped += 1
    elif status == "NOT AVAILABLE":
        missing += 1


def test(name, fn):
    global attempted
    attempted += 1
    try:
        detail = fn()
        report("PASS", name, detail)
    except Exception as exc:
        report("FAIL", name, repr(exc))


def optional_import(name):
    global attempted
    attempted += 1
    try:
        __import__(name)
        report("PASS", "Import " + name)
        return True
    except ImportError as exc:
        report("NOT AVAILABLE", "Import " + name, repr(exc))
        return False
    except Exception as exc:
        report("FAIL", "Import " + name, repr(exc))
        return False


print("\n================================================")
print(" ESP32 ABSOLUTE HARDWARE + RADIO AUDIT")
print("================================================")
print("Firmware:", sys.version)
print("Platform:", sys.platform)

# 1. Module availability: standard MicroPython + common ESP32 libraries.
print("\n--- 1. MODULE AVAILABILITY ---")
modules = (
    "array", "binascii", "builtins", "cmath", "collections", "errno",
    "gc", "hashlib", "heapq", "io", "json", "math", "os", "random",
    "re", "select", "socket", "struct", "sys", "time",
    "micropython", "machine", "esp32", "network", "bluetooth",
    "uasyncio", "framebuf", "uctypes", "vfs", "onewire", "ds18x20",
    "dht", "neopixel", "ntptime", "ssl", "requests", "urequests",
    "websocket", "webrepl", "espnow", "cryptolib", "deflate",
    "hashlib", "uhashlib", "ubinascii", "ujson", "ure", "ustruct",
    "utime", "uselect", "uos", "uarray", "uzlib", "zlib",
    "ssd1306", "sh1106", "lcd_api", "i2c_lcd", "umqtt", "aioble",
    "logging", "traceback", "threading", "pathlib", "tempfile"
)
for mod in modules:
    optional_import(mod)

# 2. Core functional tests.
print("\n--- 2. CORE FUNCTIONAL TESTS ---")


def test_math():
    import math
    assert math.sqrt(81) == 9
    assert abs(math.sin(0)) < 0.000001
    return "sqrt and sin passed"


def test_json():
    import json
    obj = {"esp32": True, "number": 123}
    assert json.loads(json.dumps(obj)) == obj
    return "encode/decode passed"


def test_struct():
    import struct
    raw = struct.pack("<I", 123456)
    assert struct.unpack("<I", raw)[0] == 123456
    return "binary pack/unpack passed"


def test_hash():
    import hashlib
    digest = hashlib.sha256(b"ESP32").digest()
    assert len(digest) == 32
    return "SHA-256 digest length = 32 bytes"


def test_regex():
    import re
    # Avoid relying on group(0), which can differ across implementations.
    match = re.search("[0-9]+", "ESP32-123")
    assert match is not None
    matched = match.group()
    assert matched == "123"
    return "matched " + matched


def test_filesystem():
    path = "audit_temp.txt"
    try:
        with open(path, "w") as f:
            f.write("ESP32_AUDIT_OK")
        with open(path, "r") as f:
            value = f.read()
        assert value == "ESP32_AUDIT_OK"
        return "write/read passed"
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


def test_memory():
    gc.collect()
    return str(gc.mem_free()) + " bytes free after collection"


def test_cpu():
    import machine
    return str(machine.freq()) + " Hz"


def test_unique_id():
    import machine
    uid = machine.unique_id()
    assert len(uid) > 0
    return "API works; ID deliberately not printed"


def test_raw_temp():
    import esp32
    return "raw sensor value = " + str(esp32.raw_temperature()) + \
        " (not Celsius)"


def test_nvs():
    import esp32
    nvs = esp32.NVS("audittest")
    key = "probe"
    try:
        nvs.set_i32(key, 13579)
        nvs.commit()
        assert nvs.get_i32(key) == 13579
        return "temporary key write/read passed"
    finally:
        try:
            nvs.erase_key(key)
            nvs.commit()
        except Exception:
            pass


def test_partitions():
    import esp32
    p = esp32.Partition
    found = []
    for attr in ("TYPE_APP", "TYPE_DATA"):
        if hasattr(p, attr):
            try:
                for item in p.find(getattr(p, attr)):
                    found.append(str(item.info()))
            except Exception as exc:
                found.append(attr + ": " + repr(exc))
    return str(found) if found else "API exists; no entries enumerated"


def test_async():
    import uasyncio as asyncio

    async def worker():
        await asyncio.sleep_ms(1)
        return 42

    value = asyncio.run(worker())
    assert value == 42
    return "async task returned 42"


def test_socket():
    import socket
    sock = socket.socket()
    sock.close()
    return "created and closed; no data sent"


for name, fn in (
    ("Math", test_math),
    ("JSON", test_json),
    ("Binary struct", test_struct),
    ("SHA-256", test_hash),
    ("Regular expressions", test_regex),
    ("Filesystem write/read/delete", test_filesystem),
    ("Garbage collector", test_memory),
    ("CPU frequency", test_cpu),
    ("Unique ID API", test_unique_id),
    ("Raw internal temperature API", test_raw_temp),
    ("NVS temporary key", test_nvs),
    ("Partition discovery", test_partitions),
    ("Async task", test_async),
    ("Socket create/close", test_socket),
):
    test(name, fn)

# 3. GPIO, ADC, PWM, I2C, SPI and UART API tests.
# Pins are only used briefly and are not connected to external loads.
print("\n--- 3. GPIO / ADC / PWM / BUS API TESTS ---")


def test_gpio():
    import machine
    pin = machine.Pin(18, machine.Pin.OUT)
    pin.value(0)
    pin.value(1)
    pin.value(0)
    pin.init(machine.Pin.IN)
    return "GPIO18 output toggle then input; no external load"


def test_adc():
    import machine
    adc = machine.ADC(machine.Pin(34))
    try:
        adc.atten(machine.ADC.ATTN_11DB)
    except Exception:
        pass
    value = adc.read()
    return "GPIO34 ADC read = " + str(value) + " (floating input; not meaningful voltage)"


def test_pwm():
    import machine
    pwm = machine.PWM(machine.Pin(18), freq=1000, duty=0)
    try:
        pwm.duty(0)
    finally:
        pwm.deinit()
    return "PWM object created at 1 kHz, duty kept at 0, then deinitialized"


def test_i2c():
    import machine
    # Classic ESP32 DevKit defaults; scan is read-only.
    bus = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
    devices = bus.scan()
    return "I2C scan on SDA21/SCL22 found addresses: " + str(devices)


def test_soft_i2c():
    import machine
    if not hasattr(machine, "SoftI2C"):
        raise RuntimeError("SoftI2C not exposed")
    bus = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
    return "SoftI2C object created; scan: " + str(bus.scan())


def test_spi():
    import machine
    spi = machine.SPI(
        2, baudrate=100000, polarity=0, phase=0,
        sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19)
    )
    spi.deinit()
    return "SPI bus object created/deinitialized; no transfer attempted"


def test_uart():
    import machine
    uart = machine.UART(2, baudrate=9600, tx=17, rx=16)
    uart.deinit()
    return "UART2 object created/deinitialized on TX17/RX16"


def test_touch_api():
    import machine
    if not hasattr(machine, "TouchPad"):
        raise RuntimeError("TouchPad API not exposed")
    # GPIO32 is a touch-capable pin on classic ESP32.
    touch = machine.TouchPad(machine.Pin(32))
    value = touch.read()
    return "TouchPad GPIO32 read = " + str(value) + " (environment-dependent)"


for name, fn in (
    ("GPIO18 digital output API", test_gpio),
    ("ADC GPIO34 API", test_adc),
    ("PWM API", test_pwm),
    ("Hardware I2C scan", test_i2c),
    ("Software I2C", test_soft_i2c),
    ("SPI API", test_spi),
    ("UART2 API", test_uart),
    ("Capacitive touch API", test_touch_api),
):
    test(name, fn)

# 4. Wi-Fi: scan nearby APs. No association, credentials or internet traffic.
print("\n--- 4. WI-FI RADIO SCAN ---")


def test_wifi_scan():
    import network
    wlan = network.WLAN(network.STA_IF)
    was_active = wlan.active()
    try:
        wlan.active(True)
        time.sleep_ms(300)
        results = wlan.scan()
        print("  Nearby Wi-Fi networks found:", len(results))
        # Print only SSID, RSSI, channel, security; no credentials exist.
        for row in results[:15]:
            try:
                ssid = row[0]
                if isinstance(ssid, bytes):
                    ssid = ssid.decode("utf-8", "replace")
                print("  AP:", repr(ssid), "RSSI:", row[3],
                      "channel:", row[2], "auth:", row[4])
            except Exception:
                print("  AP entry:", repr(row))
        return "scan completed; no network joined"
    finally:
        try:
            wlan.disconnect()
        except Exception:
            pass
        wlan.active(was_active)


test("Wi-Fi scan", test_wifi_scan)

# 5. BLE: scan advertisements for 5 seconds; no pairing/connection.
print("\n--- 5. BLUETOOTH LE SCAN ---")


def test_ble_scan():
    import bluetooth
    ble = bluetooth.BLE()
    was_active = ble.active()
    found = []

    def callback(event, data):
        # IRQ_SCAN_RESULT = 5 in MicroPython BLE API.
        if event == 5:
            try:
                addr_type, addr, adv_type, rssi, adv_data = data
                item = (bytes(addr), rssi, adv_type)
                if item not in found:
                    found.append(item)
            except Exception:
                pass

    try:
        ble.active(True)
        ble.irq(callback)
        # Duration is milliseconds. Active scan requests scan responses.
        ble.gap_scan(5000, 30000, 30000, True)
        time.sleep_ms(5500)
        ble.gap_scan(None)
        print("  BLE advertisements/devices observed:", len(found))
        for addr, rssi, adv_type in found[:15]:
            print("  BLE:", ":".join("%02X" % b for b in addr),
                  "RSSI:", rssi, "adv_type:", adv_type)
        return "scan completed; no pairing or connection attempted"
    finally:
        try:
            ble.gap_scan(None)
        except Exception:
            pass
        try:
            ble.irq(None)
        except Exception:
            pass
        try:
            ble.active(was_active)
        except Exception:
            pass


test("BLE scan", test_ble_scan)

# 6. ESP-NOW: initialize/deinitialize only. No peer and no packet sent.
# A real send/receive test requires a second ESP32 running a receiver.
print("\n--- 6. ESP-NOW API TEST ---")


def test_espnow():
    import network
    import espnow

    wlan = network.WLAN(network.STA_IF)
    was_active = wlan.active()
    e = None
    try:
        wlan.active(True)
        e = espnow.ESPNow()
        e.active(True)
        # Inspect supported methods to help diagnose firmware API differences.
        methods = [x for x in dir(e) if not x.startswith("_")]
        return "ESPNow activated successfully; methods=" + str(methods)
    finally:
        if e is not None:
            try:
                e.active(False)
            except Exception:
                pass
        try:
            wlan.active(was_active)
        except Exception:
            pass


test("ESP-NOW init/activate/deactivate", test_espnow)

# 7. List Python/MPY files from import paths.
print("\n--- 7. INSTALLED .PY / .MPY FILE DISCOVERY ---")
seen = []
for path in sys.path:
    directory = path if path else "."
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".py") or filename.endswith(".mpy"):
                entry = directory.rstrip("/") + "/" + filename
                if entry not in seen:
                    seen.append(entry)
                    print("  FILE:", entry)
    except Exception:
        pass
print("Files found in searched import paths:", len(seen))

# 8. Summary.
gc.collect()
print("\n================================================")
print(" FINAL AUDIT SUMMARY")
print("================================================")
print("Passed:", passed)
print("Failed:", failed)
print("Skipped:", skipped)
print("Modules/APIs not available:", missing)
print("Checks attempted:", attempted)
print("Free heap after audit:", gc.mem_free(), "bytes")
print("================================================")
print("IMPORTANT:")
print("- Wi-Fi scan tests reception, not internet access.")
print("- BLE scan tests reception, not pairing or GATT services.")
print("- ESP-NOW test initializes the API but sends no packets.")
print("- I2C scan only detects devices that acknowledge.")
print("- ADC on an unconnected pin gives a floating/noisy reading.")
print("- A software/API pass is not proof of attached hardware.")
print("- No partitions were erased or formatted.")
print("AUDIT COMPLETE")
