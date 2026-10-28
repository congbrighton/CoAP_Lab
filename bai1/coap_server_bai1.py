import asyncio
import datetime
import aiocoap
import aiocoap.resource as resource

class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.last_message = "Xin chao tu CoAP Server"

    async def render_get(self, request):
        payload = self.last_message.encode('utf-8')
        return aiocoap.Message(payload=payload)

    async def render_post(self, request):
        received_time = datetime.datetime.now().strftime("%H:%M:%S")
        text = request.payload.decode('utf-8')
        print("\nPOST request received:")
        print(f"Payload: {text}")
        print(f"Time: {received_time}")

        # Lưu lại thông điệp gần nhất
        self.last_message = text

        response_payload = "Server da nhan thong diep".encode('utf-8')
        return aiocoap.Message(code=aiocoap.CHANGED, payload=response_payload)

async def main():
    root = resource.Site()
    # Khai báo đường dẫn tài nguyên: /iot/lab/message
    root.add_resource(['iot', 'lab', 'message'], MessageResource())

    await aiocoap.Context.create_server_bound(root, bind=('127.0.0.1', 5683))
    print("CoAP Server started on port 5683")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
