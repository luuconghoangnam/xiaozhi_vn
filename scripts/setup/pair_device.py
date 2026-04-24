import asyncio
import websockets
import json
import uuid
import ssl

async def get_pair_code():
    # URL chinh thuc
    uri = "wss://api.xiaozhi.me/v1/robot/protocol"
    
    # Tao Device ID tu MAC cua ban
    mac_addr = hex(uuid.getnode()).replace('0x', '').upper()
    device_id = f"XZ_VN_{mac_addr[:8]}"
    
    print(f"\n[>] Device ID: {device_id}")
    print(f"[>] Dang ket noi den Server (Security Mode)...")
    
    # Bo qua kiem tra SSL neu may ban bi loi chung chi
    ssl_context = ssl._create_unverified_context()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (ESP32)",
        "X-Device-Id": device_id,
        "X-Protocol-Version": "3"
    }
    
    try:
        async with websockets.connect(
            uri, 
            extra_headers=headers,
            ssl=ssl_context,
            subprotocols=["binary", "base64"] # Xiaozhi yeu cau subprotocol
        ) as websocket:
            hello = {
                "type": "hello",
                "version": 3,
                "transport": "websocket",
                "audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 60},
                "device_id": device_id
            }
            await websocket.send(json.dumps(hello))
            
            # Nhan phan hoi
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            data = json.loads(response)
            
            if "bind_code" in data:
                print("\n" + "!"*50)
                print(f"   MA XAC THUC 6 SO CUA BAN: {data['bind_code']}")
                print("!"*50)
                print("\n[>] Hay nhap ma nay len Web ngay bay gio.")
                return True
                
    except Exception as e:
        print(f"\n[!] Khong the lay ma tu dong: {e}")
        print("\n[MEOTRUOC]: Ban hay thu MO UNG DUNG CHINH (CHAY_COONIE.bat).")
        print("Khi ung dung chay lan dau, no cung se tu dong hien ma 6 so.")
        
    return False

if __name__ == "__main__":
    asyncio.run(get_pair_code())
