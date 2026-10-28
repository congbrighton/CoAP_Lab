import asyncio
import json
import random
import aiocoap
import aiocoap.resource as resource

class SensorDataResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.data = {
            "device_id": "sensor01",
            "temperature": 28.5,
            "humidity": 65.2
        }

    async def render_get(self, request):
        payload = json.dumps(self.data).encode('utf-8')
        # Format 50 đại diện cho application/json trong CoAP
        return aiocoap.Message(payload=payload, content_format=50)

    def update_sensor_data(self):
        self.data["temperature"] = round(random.uniform(25.0, 40.0), 1)
        self.data["humidity"] = round(random.uniform(30.0, 80.0), 1)
        print(f"[Update] New Sensor Data: Temp={self.data['temperature']}°C, Hum={self.data['humidity']}%")

async def sensor_updater(sensor_resource):
    while True:
        await asyncio.sleep(3)
        sensor_resource.update_sensor_data()

async def main():
    root = resource.Site()
    sensor_res = SensorDataResource()
    root.add_resource(['iot', 'lab', 'sensor01', 'data'], sensor_res)

    await aiocoap.Context.create_server_bound(root, bind=('127.0.0.1', 5683))
    print("Sensor CoAP Server started on port 5683...")

    # Chạy vòng lặp cập nhật cảm biến liên tục mỗi 3 giây
    asyncio.create_task(sensor_updater(sensor_res))
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor Server stopped.")
