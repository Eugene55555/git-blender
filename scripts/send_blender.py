#!/usr/bin/env python3
"""Send a Python code file to the Blender MCP addon socket and print the result.

Usage: send_blender.py <file.py> [--timeout 240]
"""
import json
import socket
import sys


def main():
    if len(sys.argv) < 2:
        print("usage: send_blender.py <file.py> [--timeout N]")
        return 1
    path = sys.argv[1]
    timeout = 240.0
    if "--timeout" in sys.argv:
        timeout = float(sys.argv[sys.argv.index("--timeout") + 1])

    code = open(path, "r", encoding="utf-8").read()
    s = socket.create_connection(("127.0.0.1", 9876), timeout=30)
    s.sendall(json.dumps({"type": "execute_code", "params": {"code": code}}).encode("utf-8"))
    s.settimeout(timeout)
    buf = b""
    while True:
        try:
            chunk = s.recv(1 << 20)
        except socket.timeout:
            print("SOCKET TIMEOUT")
            break
        if not chunk:
            break
        buf += chunk
        try:
            obj = json.loads(buf.decode("utf-8"))
            break
        except Exception:
            continue
    s.close()
    try:
        out = json.loads(buf.decode("utf-8"))
    except Exception:
        print("RAW:", buf[:2000])
        return 1
    print("status:", out.get("status"))
    res = out.get("result", out.get("message"))
    print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
    return 0 if out.get("status") == "success" else 2


if __name__ == "__main__":
    sys.exit(main())
