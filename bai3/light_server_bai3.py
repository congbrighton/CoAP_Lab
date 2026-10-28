import asyncio
import json
import aiocoap
import aiocoap.resource as resource

class SmartLightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.state = "OFF"
        self.device_id = "light01"

    async def render_get(self, request):
        payload_data = {"device_id": self.device_id, "status": self.state}
        payload = json.dumps(payload_data).encode('utf-8')
        return aiocoap.Message(payload=payload, content_format=50)

    async def render_put(self, request):
        try:
            body = json.loads(request.payload.decode('utf-8'))
            command = body.get("command")

            if command in ["ON", "OFF"]:
                old_state = self.state
                if old_state != command:
                    self.state = command
                    print(f"\nPUT request received:\nDevice: {self.device_id}\nCommand: {command}")
                    print(f"Light state changed: {old_state} -> {self.state}")
                    print(f"Notify observers: {self.state}")
                    # Phát thông báo tới các Client đang Observe
                    self.updated_state()
                else:
                    print(f"\nPUT request received: Command {command} (No state change)")

                return aiocoap.Message(code=aiocoap.CHANGED)
            else:
                return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Loi: Command phai la ON hoac OFF")
        except Exception as e:
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=str(e).encode('utf-8'))

    def notify_observe_subscribers(self, obs_node):
        print("New Observe registration received")

async def main():
    root = resource.Site()
    root.add_resource(['iot', 'lab', 'light01', 'status'], SmartLightResource())

    await aiocoap.Context.create_server_bound(root, bind=('127.0.0.1', 5683))
    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status\n")

    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSmart Light Server stopped.")
