import os
import sys
import numpy as np
import sherpa_onnx
import sounddevice as sd
import json
from pathlib import Path

def get_input_device():
    try:
        with open("config/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("AUDIO_DEVICES", {}).get("input_device_id")
    except:
        return None

def test_full_asr():
    print("=== CHƯƠNG TRÌNH KIỂM TRA NHẬN DIỆN GIỌNG NÓI (ASR + KWS) ===")
    
    model_dir = Path("models")
    encoder = str(model_dir / "encoder.onnx")
    decoder = str(model_dir / "decoder.onnx")
    joiner = str(model_dir / "joiner.onnx")
    tokens = str(model_dir / "tokens.txt")
    keywords_file = str(model_dir / "keywords.txt")
    
    # 1. Khởi tạo Online Recognizer
    print("Đang nạp bộ nhận diện ASR...")
    try:
        recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
            tokens=tokens,
            encoder=encoder,
            decoder=decoder,
            joiner=joiner,
            num_threads=4,
            sample_rate=16000,
            feature_dim=80,
            decoding_method="greedy_search",
            provider="cpu",
        )
        
        # 2. Khởi tạo Keyword Spotter
        spotter = sherpa_onnx.KeywordSpotter(
            tokens=tokens,
            encoder=encoder,
            decoder=decoder,
            joiner=joiner,
            keywords_file=keywords_file,
            num_threads=4,
            sample_rate=16000,
            feature_dim=80,
            keywords_score=1.0,
            keywords_threshold=0.01,
        )
        print("Nạp model thành công!")
    except Exception as e:
        print(f"LỖI nạp model: {e}")
        return

    device_id = get_input_device()
    print(f"\nMic đang dùng: {device_id}")

    asr_stream = recognizer.create_stream()
    kws_stream = spotter.create_stream()
    
    print("\n--- BẮT ĐẦU TEST ---")
    print("Hãy nói bất cứ câu gì để xem AI nghe ra chữ gì...")
    print("Nhấn Ctrl+C để thoát.\n")

    last_text = ""

    def callback(indata, frames, time, status):
        nonlocal last_text
        samples = indata.flatten()
        
        # KWS
        kws_stream.accept_waveform(16000, samples)
        while spotter.is_ready(kws_stream):
            spotter.decode_stream(kws_stream)
        kws_result = spotter.get_result(kws_stream)
        if kws_result:
            # result có thể là object hoặc string tùy version
            res_str = getattr(kws_result, 'keyword', str(kws_result))
            print(f"\n\n[WAKE WORD DETECTED]: {res_str}\n")

        # ASR
        asr_stream.accept_waveform(16000, samples)
        while recognizer.is_ready(asr_stream):
            recognizer.decode_stream(asr_stream)
        
        asr_result = recognizer.get_result(asr_stream)
        # Sửa lỗi: lấy text an toàn
        if hasattr(asr_result, 'text'):
            text = asr_result.text
        else:
            text = str(asr_result)
            
        if text and text != last_text:
            print(f"\rAI nghe được: {text}", end="")
            last_text = text

    try:
        with sd.InputStream(device=device_id, samplerate=16000, channels=1, dtype='float32', callback=callback):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\nKết thúc test.")

if __name__ == "__main__":
    test_full_asr()
