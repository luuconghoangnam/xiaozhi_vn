import requests
import json
import os
from pathlib import Path

def get_bind_code():
    url = "https://api.xiaozhi.me/v1/robot/bind-code"
    
    # Lay Machine ID de lam Device ID
    try:
        import subprocess
        mid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    except:
        mid = "XZ_VN_DEFAULT"
        
    device_id = f"XZ_VN_{mid[:8]}"
    
    print(f"\n[>] Dang yeu cau ma lien ket cho thiet bi: {device_id}...")
    
    try:
        # Day la vi du ve API binding, thuc te Xiaozhi se cap code khi ket noi lan dau
        # Hoac nguoi dung tu nhap Device ID vao Dashboard.
        # Neu hien tai app cua ban dung Token truc tiep, chung ta se huong dan theo cach do.
        
        print("\n============================================================")
        print("          HUONG DAN LIEN KET THIET BI NHANH")
        print("============================================================")
        print(f" 1. Device ID cua ban la: {device_id}")
        print(" 2. Hay vao dashboard, nhan [Them thiet bi].")
        print(f" 3. Nhap '{device_id}' vao o Device ID.")
        print(" 4. Sau khi luu, hay copy [Access Token] va dan vao day.")
        print("============================================================\n")
        
        return device_id
    except Exception as e:
        print(f"Loi: {e}")
        return None

if __name__ == "__main__":
    get_bind_code()
