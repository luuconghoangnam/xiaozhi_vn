import asyncio
import websockets
import json
import uuid
import sys

async def get_pair_code():
    uri = "wss://api.xiaozhi.me/v1/robot/protocol"
    # Tao Device ID duy nhat
    mac_addr = hex(uuid.getnode()).replace('0x', '').upper()
    device_id = f"XZ_VN_{mac_addr[:8]}"
    
    print(f"\n[>] Dang ket noi den server Xiaozhi...")
    try:
        async with websockets.connect(uri) as websocket:
            # Gui thong tin hello de xin ma bind
            hello = {
                "type": "hello",
                "version": 3,
                "transport": "websocket",
                "audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 60},
                "device_id": device_id
            }
            await websocket.send(json.dumps(hello))
            
            # Cho phan hoi tu server
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "hello" and "bind_code" in data:
                bind_code = data["bind_code"]
                print("\n" + "="*50)
                print(f"       MA LIEN KET CUA BAN LA: {bind_code}")
                print("="*50)
                print("\n1. Hay nhap ma 6 so nay vao Web Xiaozhi.")
                print("2. Sau khi nhap xong, nhan phim bat ky o day de tiep tuc.")
                return True
            else:
                # Neu server yeu cau token nghia la da bind roi
                print(f"\n[!] Thiet bi nay da duoc lien ket truoc do (Device ID: {device_id})")
                return False
                
    except Exception as e:
        print(f"\n[!] Loi ket noi: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(get_pair_code())
