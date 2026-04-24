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
  <a href="#-lấy-access-token">Lấy Token</a> •
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
- **Nhận diện hình ảnh**: Coonie có thể nhìn qua Camera để mô tả đồ vật, đọc chữ hoặc phân tích tình huống thông qua các mô hình Vision.

## 🚀 Cài đặt

### Cách 1: Sử dụng Script tự động (Khuyên dùng - Tự động 100%)
1. Tải dự án về máy:
   ```bash
   git clone https://github.com/luuconghoangnam/xiaozhi_vn.git
   cd xiaozhi_vn/py-xiaozhi
   ```
2. **Windows**: Chạy file `install.bat`.
3. **Linux/macOS**: Chạy lệnh `python3 install.py`.

Script sẽ tự động tạo môi trường ảo, cài đặt thư viện và **tự động tải Models**.

## 🔑 Lấy Access Token

Để ứng dụng có thể kết nối với server AI, bạn cần có một Access Token:

1. Truy cập vào trang quản lý: [https://xiaozhi.me/](https://xiaozhi.me/) (hoặc quét mã QR trên thiết bị nếu có).
2. Đăng nhập vào tài khoản của bạn.
3. Tìm đến mục **Thiết bị (Devices)** hoặc **Cài đặt (Settings)**.
4. Sao chép đoạn mã **Access Token** (thường là một chuỗi ký tự dài).

## ⚙️ Cấu hình

Sau khi đã có Token, bạn thực hiện điền vào ứng dụng như sau:

1. Tìm file `config/config.json` trong thư mục dự án.
2. Mở file bằng Notepad hoặc VS Code.
3. Tìm dòng `"WEBSOCKET_ACCESS_TOKEN": "..."` và dán Token của bạn vào giữa dấu ngoặc kép.
   ```json
   "NETWORK": {
     "WEBSOCKET_ACCESS_TOKEN": "DÁN_TOKEN_CỦA_BẠN_VÀO_ĐÂY",
     ...
   }
   ```
4. Lưu file lại.

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
Chúng tôi luôn hoan nghênh các đóng góp từ cộng đồng.

## 📄 Giấy phép
Phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.

---
**XiaoZhi VN** - Mang sức mạnh AI đến gần hơn với người dùng Việt! 🇻🇳
