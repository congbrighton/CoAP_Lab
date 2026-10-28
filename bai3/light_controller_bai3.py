import asyncio
import json
import aiocoap
from aiocoap import Context, Message, GET, PUT

async def main():
    protocol = await Context.create_client_context()
    uri = 'coap://localhost:5683/iot/lab/light01/status'

    while True:
        loop = asyncio.get_running_loop()
        cmd = await loop.run_in_executor(None, input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
        cmd = cmd.strip().upper()

        if cmd == "EXIT":
            print("Thoat chương trình.")
            break

        elif cmd == "STATUS":
            print("\nSending GET request...")
            req = Message(code=GET, uri=uri)
            try:
                res = await protocol.request(req).response
                print(f"Response:\n{res.payload.decode('utf-8')}\n")
            except Exception as e:
                print(f"Lỗi: {e}\n")

        elif cmd in ["ON", "OFF"]:
            print("\nSending PUT request...")
            payload_data = {"device_id": "light01", "command": cmd}
            payload = json.dumps(payload_data).encode('utf-8')
            req = Message(code=PUT, uri=uri, payload=payload, content_format=50)

            try:
                res = await protocol.request(req).response
                print(f"Response Code: {res.code}")
                if res.code == aiocoap.CHANGED:
                    action = "bat" if cmd == "ON" else "tat"
                    print(f"Da {action} den light01\n")
                else:
                    print(f"Lỗi từ server: {res.payload.decode('utf-8')}\n")
            except Exception as e:
                print(f"Lỗi: {e}\n")
        else:
            print("Lệnh không hợp lệ! Vui lòng nhập ON, OFF, STATUS hoặc EXIT.\n")

if __name__ == "__main__":
    asyncio.run(main())
