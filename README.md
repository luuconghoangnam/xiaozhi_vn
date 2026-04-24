<p align="center">
  <img src="./assets/logo.png" alt="XiaoZhi VN Logo" width="200"/>
</p>

<h1 align="center">🤖 XiaoZhi VN (Coonie AI)</h1>

<p align="center">
  <strong>Trợ lý AI tiếng Việt thông minh cho máy tính của bạn</strong>
</p>

<p align="center">
  <a href="#-tính-năng-nổi-bật">Tính năng</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-cấu-hình">Cấu hình</a> •
  <a href="#-mcp-tools">Công cụ</a> •
  <a href="#-đóng-góp">Đóng góp</a>
</p>

---

**XiaoZhi VN** là phiên bản Việt hóa và mở rộng của dự án [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi). Dự án này mang đến một trợ lý AI có khả năng nghe, nói, nhìn và điều khiển máy tính hoàn toàn bằng tiếng Việt. 

Đặc biệt, phiên bản này được tinh chỉnh với nhân vật **Coonie** - một cô gái AI thân thiện, ngọt ngào và vô cùng thông minh.

## ✨ Tính năng nổi bật

### 🎙️ Tương tác Giọng nói (Voice Interaction)
- **Đánh thức bằng giọng nói (Wake Word)**: Sử dụng Sherpa-ONNX để nhận diện từ khóa (VD: "Coonie ơi") hoàn toàn offline.
- **Hỗ trợ Tiếng Việt**: Nhận diện và phản hồi bằng tiếng Việt tự nhiên, trôi chảy.
- **VAD (Voice Activity Detection)**: Tự động phát hiện khi bạn bắt đầu và kết thúc câu nói.

### 👁️ Đa phương thức (Multimodal Vision)
- **Nhận diện hình ảnh**: Coonie có thể nhìn qua Camera để mô tả đồ vật, đọc chữ hoặc phân tích tình huống thông qua các mô hình Vision (như GLM-4V).

### 🛠️ Hệ sinh thái công cụ (MCP Tools)
- **Điều khiển hệ thống**: Tăng giảm âm lượng, tắt máy, chụp màn hình.
- **Giải trí**: Tìm kiếm và phát nhạc từ Youtube, quản lý thư viện nhạc local.
- **Thông tin**: Xem thời tiết, tra cứu kiến thức, quản lý lịch trình cá nhân.

### 🖥️ Giao diện hiện đại
- Giao diện PyQt5 trực quan với các biểu cảm sinh động của trợ lý AI.
- Chế độ chạy ngầm trong khay hệ thống (System Tray).

## 🚀 Cài đặt

### Cách 1: Sử dụng Script tự động (Khuyên dùng)
1. Tải dự án về máy:
   ```bash
   git clone https://github.com/your-username/xiaozhi_vn.git
   cd xiaozhi_vn/py-xiaozhi
   ```
2. **Windows**: Double-click vào file `install.bat`.
3. **Linux/macOS**: Chạy lệnh `python3 install.py`.

Script sẽ tự động tạo môi trường ảo, cài đặt thư viện và chuẩn bị file cấu hình.

### Cách 2: Cài đặt thủ công
1. Tạo môi trường ảo: `python -m venv .venv`
2. Kích hoạt: `.venv\Scripts\activate` (Windows) hoặc `source .venv/bin/activate` (Mac/Linux).
3. Cài đặt thư viện: `pip install -r requirements.txt`

## ⚙️ Cấu hình

Sau khi cài đặt, bạn cần thực hiện các bước sau:
1. Mở file `config/config.json`.
2. Điền **WEBSOCKET_ACCESS_TOKEN** (Lấy từ hệ thống XiaoZhi).
3. (Tùy chọn) Điền **VLapi_key** nếu bạn muốn sử dụng tính năng Camera.
4. Kiểm tra thư mục `models/` đã có đủ các file: `encoder.onnx`, `decoder.onnx`, `joiner.onnx`, `tokens.txt`.

## 🏃 Chạy ứng dụng

Chạy lệnh sau để khởi động:
```bash
python main.py
```

## 📂 Cấu trúc thư mục
- `src/`: Mã nguồn chính của ứng dụng.
- `config/`: Chứa cấu hình và dữ liệu kích hoạt (Được bảo mật, không đẩy lên git).
- `models/`: Chứa các mô hình AI cho nhận diện giọng nói.
- `assets/`: Hình ảnh, icon và tài nguyên giao diện.

## 🤝 Đóng góp
Chúng tôi luôn hoan nghênh các đóng góp từ cộng đồng:
1. Fork dự án.
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`).
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`).
4. Push lên nhánh (`git push origin feature/AmazingFeature`).
5. Mở một Pull Request.

## 📄 Giấy phép
Phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.

---
**XiaoZhi VN** - Mang sức mạnh AI đến gần hơn với người dùng Việt! 🇻🇳
