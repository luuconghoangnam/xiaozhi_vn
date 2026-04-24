# 🤖 XiaoZhi VN - Phiên bản Việt hóa

Chào mừng bạn đến với **XiaoZhi VN**, phiên bản Việt hóa của [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi). Dự án này mang đến trải nghiệm trợ lý AI thông minh (tương tự ESP32 XiaoZhi) ngay trên máy tính của bạn với sự hỗ trợ tiếng Việt hoàn chỉnh.

## ✨ Tính năng nổi bật

- **Giao diện tiếng Việt**: Toàn bộ giao diện và phản hồi được tối ưu cho người dùng Việt Nam.
- **Đánh thức bằng giọng nói (Wake Word)**: Sử dụng Sherpa-ONNX offline, phản hồi nhanh và bảo mật.
- **Đa phương thức (Vision)**: Nhận diện hình ảnh qua Camera.
- **Hệ sinh thái MCP Tools**: Điều khiển máy tính, nghe nhạc Youtube, quản lý lịch trình, xem thời tiết...
- **Hỗ trợ đa nền tảng**: Chạy tốt trên Windows, macOS và Linux.

## 🚀 Hướng dẫn cài đặt nhanh

### 1. Yêu cầu hệ thống
- Python 3.9 - 3.12
- Microphone và Loa/Tai nghe.

### 2. Tải mã nguồn
```bash
git clone https://github.com/your-username/xiaozhi_vn.git
cd xiaozhi_vn/py-xiaozhi
```

### 3. Cài đặt môi trường
Khuyên dùng môi trường ảo (venv):
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Cấu hình
1. Copy file cấu hình mẫu:
   ```bash
   cp config/config.example.json config/config.json
   ```
2. Mở `config/config.json` và điền các thông tin cần thiết (Access Token, API Key nếu có).

### 5. Tải Model (Quan trọng)
Bạn cần tải các model cho Sherpa-ONNX và đặt vào thư mục `models/`. 
Các file cần thiết bao gồm: `encoder.onnx`, `decoder.onnx`, `joiner.onnx`, `tokens.txt`.

### 6. Chạy chương trình
```bash
python main.py
```

## 🛠 Công cụ hỗ trợ (MCP)
Dự án tích hợp sẵn các công cụ:
- `audio`: Phát nhạc từ Youtube/Local.
- `system_control`: Điều khiển âm lượng, tắt máy, chụp màn hình.
- `weather`: Xem thời tiết tại Việt Nam.

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.

---
**Lưu ý**: Đây là dự án đang phát triển. Mọi đóng góp (Pull Request) đều được chào đón!
