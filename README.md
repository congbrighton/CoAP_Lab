# CoAP_Lab
# BÁO CÁO THỰC HÀNH LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

## Thông tin sinh viên
- **Họ và tên:** Nguyễn Đức Công
- **Mã sinh viên:** B23DCCN102

---

## Cấu trúc thư mục
```text
CoAP_Lab/
├── bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
├── bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
├── bai3/
│   ├── light_server_bai3.py
│   ├── light_controller_bai3.py
│   └── light_monitor_bai3.py
└── README.md
Môi trường phát triểnNgôn ngữ: Python 3.x (khuyến nghị phiên bản 3.9 trở lên).Thư viện chính: aiocoapGiao thức: CoAP chạy trên nền UDP (cổng mặc định 5683). Không yêu cầu cài đặt MQTT Broker hay RabbitMQ. Server và Client được cài đặt hoàn toàn bằng Python.Cài đặt thư việnBashpip install aiocoap
Địa chỉ, Cổng và URI tài nguyênThông số hệ thốngThông sốGiá trịĐịa chỉ Serverlocalhost (127.0.0.1)Cổng lắng nghe5683 (UDP)Danh sách Tài nguyên (URI)BàiURI tài nguyênPhương thức hỗ trợ1coap://localhost:5683/iot/lab/messageGET, POST2coap://localhost:5683/iot/lab/sensor01/dataGET3coap://localhost:5683/iot/lab/light01/statusGET, PUT, ObserveCấu hình khi triển khai trên hai máy riêng biệtHệ thống hỗ trợ đọc địa chỉ IP từ biến môi trường mà không cần thay đổi mã nguồn:Biến môi trườngDùng ởGiá trị mặc địnhÝ nghĩaCOAP_BINDServerlocalhostĐịa chỉ Server lắng nghe (đặt 0.0.0.0 hoặc IP máy để nhận kết nối từ ngoài)COAP_HOSTClientlocalhostĐịa chỉ IP của máy chạy ServerThiết lập biến môi trườngWindows (PowerShell):PowerShell$env:COAP_BIND="0.0.0.0"      # Chạy trên máy Server
$env:COAP_HOST="192.168.1.10" # Chạy trên máy Client
Linux / macOS:Bashexport COAP_BIND=0.0.0.0
export COAP_HOST=192.168.1.10
Lưu ý: Cần đảm bảo tường lửa cho phép kết nối qua cổng UDP 5683 trên máy chạy Server.Hướng dẫn vận hànhMỗi chương trình chạy trong một terminal riêng biệt. Luôn chạy Server trước, sau đó mới chạy Client. Để dừng các chương trình chạy liên tục, nhấn Ctrl + C.Bài 1: Gửi và nhận thông điệp CoAP cơ bảnBashcd bai1
python coap_server_bai1.py
python coap_client_bai1.py
coap_server_bai1.py: Khởi tạo Server tại tài nguyên /iot/lab/message.Phương thức GET: Trả về nội dung Xin chao tu CoAP Server.Phương thức POST: Nhận thông điệp, in ra màn hình thông tin nhận được kèm thời điểm nhận, sau đó trả về mã 2.04 Changed với nội dung Server da nhan thong diep.coap_client_bai1.py: Gửi yêu cầu GET, sau đó gửi yêu cầu POST chứa thông tin sinh viên (B23DCCN102 - Nguyễn Đức Công). Hiển thị mã phản hồi và payload trả về. Tự động xử lý và báo lỗi kết nối nếu Server ngừng hoạt động.Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩmBashcd bai2
python sensor_server_bai2.py
python monitor_client_bai2.py
sensor_server_bai2.py: Cung cấp tài nguyên /iot/lab/sensor01/data, tự động sinh và cập nhật giá trị nhiệt độ (25.0 - 40.0°C) và độ ẩm (30.0 - 80.0%) ngẫu nhiên sau mỗi 3 giây. Trả về dữ liệu JSON với Content-Format là application/json:JSON{"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
monitor_client_bai2.py: Định kỳ gửi yêu cầu GET mỗi 3 giây, hiển thị dữ liệu nhận được kèm cảnh báo:Nhiệt độ > 35°C: CANH BAO: Nhiet do caoĐộ ẩm < 40%: CANH BAO: Do am thapBình thường: Trang thai: Binh thuongNếu Server không phản hồi, Client thông báo lỗi và tiếp tục thử lại ở chu kỳ tiếp theo.Bài 3: Giám sát và điều khiển đèn thông minh bằng CoAP ObserveChạy chương trình ở 3 cửa sổ terminal riêng biệt:Bash# Terminal 1 - Server
cd bai3
python light_server_bai3.py

# Terminal 2 - Monitor (Quan sát)
cd bai3
python light_monitor_bai3.py

# Terminal 3 - Controller (Điều khiển)
cd bai3
python light_controller_bai3.py
light_server_bai3.py: Cung cấp tài nguyên /iot/lab/light01/status (kế thừa từ ObservableResource của aiocoap), trạng thái ban đầu là OFF.GET: Trả về trạng thái hiện tại dưới dạng JSON: {"device_id": "light01", "status": "OFF"}.PUT: Nhận câu lệnh điều khiển {"device_id": "light01", "command": "ON"} hoặc "OFF". Nếu lệnh hợp lệ, cập nhật trạng thái và phản hồi 2.04 Changed. Nếu lệnh sai, trả về lỗi 4.00 Bad Request.Khi trạng thái thực sự thay đổi, Server tự động gửi thông báo đến tất cả Client đang đăng ký Observe.light_controller_bai3.py: Cho phép người dùng nhập lệnh tương tác qua bàn phím: ON, OFF (gửi PUT), STATUS (gửi GET), hoặc EXIT (thoát).light_monitor_bai3.py: Đăng ký quan sát (Observe) tài nguyên, nhận trạng thái ban đầu và nhận thông báo cập nhật tự động từ Server mỗi khi trạng thái đèn thay đổi. Sử dụng hoàn toàn cơ chế Observe, không dùng vòng lặp GET định kỳ.Kết quả đạt đượcBài 1: Server khởi tạo thành công và xử lý chính xác các yêu cầu GET và POST. Client gửi dữ liệu thành công, hiển thị đầy đủ payload phản hồi và mã trạng thái. Chương trình có khả năng bắt và xử lý ngoại lệ khi mất kết nối tới Server.Bài 2: Server phát tài nguyên cảm biến chuẩn xác qua URI, cập nhật dữ liệu tự động mỗi 3 giây và phản hồi đúng định dạng application/json. Client phân tích dữ liệu định kỳ và đưa ra cảnh báo chính xác theo ngưỡng quy định.Bài 3: Controller điều khiển và truy vấn trạng thái thiết bị thành công thông qua PUT và GET. Monitor đăng ký cơ chế Observe thành công, tự động cập nhật khi trạng thái đèn thay đổi mà không cần truy vấn định kỳ. Các câu lệnh điều khiển sai được Server xử lý và phản hồi đúng mã lỗi 4.00 Bad Request.Log minh chứng mẫuLog mẫu Bài 1 (Server)PlaintextCoAP Server started on port 5683

GET request received: /iot/lab/message

POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN102 - Nguyễn Đức Công
Time: 10:15:20
Log mẫu Bài 2 (Client)Plaintext Received sensor data
Device: sensor01
Temperature: 36.1 C
Humidity: 38.7 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
------------------------------
Log mẫu Bài 3 (Monitor)PlaintextRegistering CoAP Observe...
Observe registration successful

 Initial State
Device: light01
Status: OFF

 State Updated
Device: light01
Status: ON
