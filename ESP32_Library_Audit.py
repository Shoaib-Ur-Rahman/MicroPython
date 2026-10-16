
# ESP32_Complete_Audit.py
# Comprehensive MicroPython module and API audit
# Target: ESP32 + MicroPython
# No external hardware required

import sys
import os
import gc
import time

passed = 0
failed = 0
skipped = 0
missing = 0
tested = 0


def report(status, name, detail=""):
    global passed, failed, skipped, missing, tested

    print(status + ": " + name)
    if detail:
        print("  " + str(detail))

    if status == "PASS":
        passed += 1
    elif status == "FAIL":
        failed += 1
    elif status == "SKIP":
        skipped += 1
    elif status == "NOT INSTALLED":
        missing += 1


def test(name, function):
    global tested
    tested += 1

    try:
        result = function()
        report("PASS", name, result)
    except Exception as e:
        report("FAIL", name, repr(e))


def import_test(name):
    global tested
    tested += 1

    try:
        __import__(name, globals(), locals(), ["*"])
        report("PASS", "Import " + name)
    except ImportError as e:
        report("NOT INSTALLED", "Import " + name, repr(e))
    except Exception as e:
        report("FAIL", "Import " + name, repr(e))


print()
print("========================================")
print(" ESP32 COMPLETE MICROPYTHON AUDIT")
print("========================================")

print("Firmware:", sys.version)
print("Platform:", sys.platform)
print("CPU frequency:", end=" ")

try:
    import machine
    print(machine.freq(), "Hz")
except Exception:
    print("unavailable")

# -------------------------------------------------
# 1. STANDARD AND COMMON MICROPYTHON MODULES
# -------------------------------------------------

print()
print("--- 1. MODULE IMPORT AUDIT ---")

modules = (
    # Core Python and data structures
    "array", "binascii", "builtins", "cmath",
    "collections", "errno", "gc", "hashlib",
    "heapq", "io", "json", "math", "os",
    "random", "re", "select", "struct",
    "sys", "time", "zlib",

    # MicroPython-specific
    "micropython", "machine", "esp32",
    "uasyncio", "asyncio", "uerrno",
    "uhashlib", "ubinascii", "ujson",
    "ure", "ustruct", "utime", "uzlib",
    "uselect", "uos", "uarray",

    # Hardware interfaces
    "network", "bluetooth", "framebuf",
    "uctypes", "vfs", "onewire", "ds18x20",
    "dht", "neopixel", "ntptime",

    # Networking and security
    "socket", "ssl", "requests", "urequests",
    "websocket", "webrepl", "webrepl_setup",

    # Common display and device libraries
    "ssd1306", "sh1106", "lcd_api",
    "i2c_lcd", "umqtt", "aioble",

    # Common utility libraries
    "platform", "logging", "traceback",
    "threading", "subprocess", "pathlib",
    "tempfile", "argparse", "unittest"
)

for module_name in modules:
    import_test(module_name)

# Nested MQTT packages are checked separately.
print()
print("--- 2. COMMON NESTED LIBRARIES ---")

for module_name in (
    "umqtt.simple",
    "umqtt.robust",
    "umqtt.simple2"
):
    import_test(module_name)

# -------------------------------------------------
# 3. STANDARD FUNCTIONAL TESTS
# -------------------------------------------------

print()
print("--- 3. CORE FUNCTIONAL TESTS ---")


def check_math():
    import math
    assert math.sqrt(81) == 9
    assert abs(math.sin(0)) < 0.000001
    return "Math operations correct"


def check_json():
    import json
    original = {"test": 123, "ok": True}
    encoded = json.dumps(original)
    decoded = json.loads(encoded)
    assert decoded["test"] == 123
    assert decoded["ok"] is True
    return "JSON encode/decode correct"


def check_struct():
    import struct
    data = struct.pack("<I", 123456)
    assert struct.unpack("<I", data)[0] == 123456
    return "Binary packing/unpacking correct"


def check_hash():
    import hashlib
    digest = hashlib.sha256(b"ESP32").digest()
    assert len(digest) == 32
    return "SHA-256 digest generated"


def check_regex():
    import re
    match = re.search(r"[0-9]+", "ESP32-123")
    assert match is not None
    assert match.group(0) == "123"
    return "Regex matching correct"


def check_collections():
    from collections import deque
    q = deque((), 3)
    q.append(10)
    q.append(20)
    assert q.popleft() == 10
    assert q.popleft() == 20
    return "Deque operations correct"


def check_array():
    from array import array
    a = array("i", [10, 20, 30])
    assert a[1] == 20
    return "Array operations correct"


def check_binary():
    import binascii
    result = binascii.hexlify(b"AB")
    assert result == b"4142"
    return "Hex conversion correct"


def check_random():
    import random
    value = random.randint(1, 100)
    assert 1 <= value <= 100
    return "Random value: " + str(value)


def check_gc():
    gc.collect()
    free = gc.mem_free()
    assert free > 0
    return str(free) + " bytes free"


test("Math", check_math)
test("JSON", check_json)
test("Struct", check_struct)
test("SHA-256", check_hash)
test("Regular expressions", check_regex)
test("Collections", check_collections)
test("Array", check_array)
test("Binary conversion", check_binary)
test("Random generator", check_random)
test("Garbage collector", check_gc)

# -------------------------------------------------
# 4. FILESYSTEM: CREATE, READ, DELETE TEST FILE
# -------------------------------------------------

print()
print("--- 4. FILESYSTEM TEST ---")


def check_filesystem():
    path = "audit_temp.txt"

    try:
        with open(path, "w") as f:
            f.write("ESP32_AUDIT_123")

        with open(path, "r") as f:
            value = f.read()

        assert value == "ESP32_AUDIT_123"
        return "Temporary file write/read correct"

    finally:
        try:
            os.remove(path)
        except Exception:
            pass


test("Filesystem write/read/delete", check_filesystem)


def check_statvfs():
    result = os.statvfs("/")
    return "Filesystem statistics available: " + str(result)


test("Filesystem information", check_statvfs)

# -------------------------------------------------
# 5. ESP32 HARDWARE AND SYSTEM APIs
# -------------------------------------------------

print()
print("--- 5. ESP32 SYSTEM API TESTS ---")


def check_cpu():
    import machine
    return str(machine.freq()) + " Hz"


def check_unique_id_api():
    import machine
    value = machine.unique_id()
    assert len(value) > 0
    return "Unique-ID API available; ID not printed"


def check_reset_cause():
    import machine
    return "Reset cause: " + str(machine.reset_cause())


def check_raw_temperature():
    import esp32
    value = esp32.raw_temperature()
    return "Raw internal sensor value: " + str(value)


def check_esp32_api():
    import esp32
    names = dir(esp32)
    assert len(names) > 0
    return str(len(names)) + " names exposed by esp32 module"


def check_machine_api():
    import machine
    names = dir(machine)
    assert "Pin" in names
    return str(len(names)) + " names exposed by machine module"


test("CPU frequency", check_cpu)
test("Unique-ID API", check_unique_id_api)
test("Reset-cause API", check_reset_cause)
test("Internal temperature sensor API", check_raw_temperature)
test("ESP32 module", check_esp32_api)
test("Machine module", check_machine_api)

# -------------------------------------------------
# 6. NON-DESTRUCTIVE PARTITION DISCOVERY
# -------------------------------------------------

print()
print("--- 6. PARTITION DISCOVERY ---")


def check_partitions():
    import esp32

    if not hasattr(esp32, "Partition"):
        raise RuntimeError("Partition API unavailable")

    partition_class = esp32.Partition
    found = []

    for kind_name in ("TYPE_APP", "TYPE_DATA"):
        if not hasattr(partition_class, kind_name):
            continue

        kind = getattr(partition_class, kind_name)

        try:
            items = partition_class.find(kind)
            for part in items:
                found.append(str(part.info()))
        except Exception as e:
            found.append(kind_name + ": " + repr(e))

    if not found:
        return "Partition API exists; no partitions enumerated"

    return "Discovered entries: " + str(found)


test("Partition discovery", check_partitions)

# -------------------------------------------------
# 7. NVS TEST USING A TEMPORARY KEY
# -------------------------------------------------

print()
print("--- 7. NVS STORAGE TEST ---")


def check_nvs():
    import esp32

    if not hasattr(esp32, "NVS"):
        raise RuntimeError("NVS API unavailable")

    nvs = esp32.NVS("audittest")
    key = "probe"

    try:
        nvs.set_i32(key, 2468)
        nvs.commit()

        value = nvs.get_i32(key)
        assert value == 2468

        return "Temporary NVS value stored and read correctly"

    finally:
        try:
            nvs.erase_key(key)
            nvs.commit()
        except Exception:
            pass


test("NVS temporary key", check_nvs)

# -------------------------------------------------
# 8. WIFI AND BLUETOOTH OBJECTS
# Radio remains inactive.
# -------------------------------------------------

print()
print("--- 8. WIRELESS API TESTS ---")


def check_wifi():
    import network

    wlan = network.WLAN(network.STA_IF)
    active = wlan.active()

    assert active is False or active is True
    return "WLAN object works; active=" + str(active)


def check_ble():
    import bluetooth

    ble = bluetooth.BLE()
    active = ble.active()

    assert active is False or active is True
    return "BLE object works; active=" + str(active)


test("Wi-Fi API", check_wifi)
test("Bluetooth API", check_ble)

# -------------------------------------------------
# 9. SOCKET API, NO DATA TRANSMITTED
# -------------------------------------------------

print()
print("--- 9. NETWORK SOCKET TEST ---")


def check_socket():
    import socket

    s = socket.socket()
    s.close()
    return "Socket created and closed without sending data"


test("Socket creation/close", check_socket)

# -------------------------------------------------
# 10. ASYNC TASK TEST
# -------------------------------------------------

print()
print("--- 10. ASYNCIO TEST ---")


def check_asyncio():
    import uasyncio as asyncio

    async def worker():
        await asyncio.sleep_ms(1)
        return 42

    result = asyncio.run(worker())
    assert result == 42
    return "Async task returned " + str(result)


test("Async task execution", check_asyncio)

# -------------------------------------------------
# 11. INSTALLED LIBRARY FILE DISCOVERY
# Does NOT import arbitrary files automatically.
# -------------------------------------------------

print()
print("--- 11. INSTALLED LIBRARY FILES ---")

found_files = []
searched_paths = []

for path in sys.path:
    if not path:
        path = "."

    if path in searched_paths:
        continue

    searched_paths.append(path)

    try:
        entries = os.listdir(path)

        for filename in entries:
            if filename.endswith(".py") or filename.endswith(".mpy"):
                if filename not in found_files:
                    found_files.append(filename)
                    print("LIBRARY FILE:", filename)

    except Exception:
        pass

print("Search paths:", searched_paths)
print("Python/MPY files found:", len(found_files))

# -------------------------------------------------
# 12. FINAL SUMMARY
# -------------------------------------------------

print()
print("========================================")
print(" COMPLETE AUDIT SUMMARY")
print("========================================")
print("Tests passed:", passed)
print("Tests failed:", failed)
print("Tests skipped:", skipped)
print("Modules not installed:", missing)
print("Total checks attempted:", tested)
print("========================================")
print("AUDIT FINISHED")
print()
print("NOTE:")
print("- Missing optional modules are not automatically faults.")
print("- Import success does not prove every API works.")
print("- Sensor/display drivers require the actual hardware.")
print("- Wi-Fi/BLE communication was not tested.")
print("- No partition was erased or formatted.")
print("- Internal temperature is a raw sensor reading.")
