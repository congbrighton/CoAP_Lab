import asyncio
import json
import datetime
import aiocoap

async def main():
    protocol = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri='coap://localhost:5683/iot/lab/light01/status', observe=0)

    print("Registering CoAP Observe...")
    req_site = protocol.request(request)

    # Lấy phản hồi đầu tiên xác nhận việc Observe
    first_response = await req_site.response
    print("Observe registration successful\n")

    is_initial = True
    async for response in req_site.observation:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        data = json.loads(response.payload.decode('utf-8'))

        tag = "Initial State" if is_initial else "State Updated"
        print(f"[{now}] {tag}")
        print(f"Device: {data.get('device_id')}")
        print(f"Status: {data.get('status')}\n")

        is_initial = False

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped Light Monitoring.")
