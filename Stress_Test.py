
import time
import gc
import machine
import network
import esp32
import socket

SSID = "SQM"
PASSWORD = "Benz2026!"

DURATION_MS = 4 * 60 * 1000
CHUNK = 10000

old_freq = machine.freq()
wlan = network.WLAN(network.STA_IF)
number = 0x12345678
iterations = 0

def http_check():
    s = None
    try:
        addr = socket.getaddrinfo(
            "example.com", 80, 0, socket.SOCK_STREAM
        )[0][-1]
        s = socket.socket()
        s.settimeout(4)
        s.connect(addr)
        s.send(b"GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
        return s.recv(80).startswith(b"HTTP/")
    except Exception as e:
        print("Network check:", e)
        return False
    finally:
        if s:
            try:
                s.close()
            except Exception:
                pass

print("4-minute CPU + Wi-Fi test")
start = time.ticks_ms()
last_report = start
last_http = start
baseline = None
highest = None
http_pass = 0
http_fail = 0
stop_reason = "Time limit reached"

try:
    machine.freq(240000000)
    gc.collect()

    baseline = esp32.raw_temperature()
    highest = baseline
    print("Baseline raw sensor:", baseline)

    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        connect_start = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), connect_start) > 20000:
                raise RuntimeError("Wi-Fi connection timeout")
            time.sleep_ms(200)

    print("Wi-Fi connected. Test running.")

    while time.ticks_diff(time.ticks_ms(), start) < DURATION_MS:
        for i in range(CHUNK):
            number = (number * 1664525 + 1013904223) & 0xFFFFFFFF
            number ^= number >> 13
            number = (number * 2246822519) & 0xFFFFFFFF
        iterations += CHUNK

        now = time.ticks_ms()

        if time.ticks_diff(now, last_report) >= 1000:
            raw = esp32.raw_temperature()
            highest = max(highest, raw)
            elapsed = time.ticks_diff(now, start) // 1000

            print("Time:", elapsed, "s | Raw:", raw,
                  "| Heap:", gc.mem_free(),
                  "| Iterations:", iterations)

            # Precaution only; NOT a calibrated thermal limit.
            if abs(raw - baseline) >= 10:
                stop_reason = "Raw sensor changed by 10 units"
                print("STOP:", stop_reason)
                break

            last_report = now

        if time.ticks_diff(now, last_http) >= 15000:
            if wlan.isconnected() and http_check():
                http_pass += 1
                print("HTTP: PASS")
            else:
                http_fail += 1
                print("HTTP: FAIL")
            last_http = time.ticks_ms()

    else:
        print("PASS: Four-minute workload completed.")

finally:
    try:
        wlan.disconnect()
        wlan.active(False)
    except Exception:
        pass

    machine.freq(old_freq)
    gc.collect()
    print("Stop reason:", stop_reason)
    print("HTTP passes/failures:", http_pass, http_fail)
    print("Total iterations:", iterations)
    print("Highest raw sensor reading:", highest)
    print("Restored CPU frequency:", machine.freq())
    print("Final free heap:", gc.mem_free())
    print("Cleanup finished.")
