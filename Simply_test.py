
import network
import time
import socket

# Enter your own Wi-Fi details
SSID = "SQM"
PASSWORD = "Benz2026!"

wlan = network.WLAN(network.STA_IF)

try:
    wlan.active(True)

    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)

    timeout = 20
    start = time.time()

    while not wlan.isconnected() and time.time() - start < timeout:
        print("Waiting...")
        time.sleep(1)

    if not wlan.isconnected():
        print("FAIL: Wi-Fi connection timed out")
    else:
        print("PASS: Wi-Fi connected")
        print("IP configuration:", wlan.ifconfig())

        # DNS lookup checks that a hostname can be resolved.
        print("Testing DNS...")
        address = socket.getaddrinfo(
            "example.com", 80, 0, socket.SOCK_STREAM
        )[0][-1]
        print("PASS: DNS lookup:", address)

        # Small HTTP request; no TLS certificate setup required.
        print("Testing HTTP...")
        sock = socket.socket()
        sock.settimeout(8)

        try:
            sock.connect(address)
            sock.send(
                b"GET / HTTP/1.1\r\n"
                b"Host: example.com\r\n"
                b"Connection: close\r\n\r\n"
            )

            response = sock.recv(256)
            print("HTTP response:", response)
            if b"200" in response or b"301" in response or b"302" in response:
                print("PASS: HTTP server responded")
            else:
                print("CHECK: Server responded; inspect status above")
        finally:
            sock.close()

except Exception as e:
    print("FAIL:", repr(e))

finally:
    try:
        wlan.disconnect()
        wlan.active(False)
        print("Wi-Fi disconnected")
    except Exception:
        pass
