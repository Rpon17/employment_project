from pydub import AudioSegment
from pathlib import Path

def mix_audio(original_path: str, bass_path: str, output_path: Path, bass_gain_db: float = 3.0):
    """
    🎧 원곡과 베이스 트랙을 섞어 새로운 믹스 파일을 생성
    """
    try:
        song = AudioSegment.from_file(original_path)
        bass = AudioSegment.from_file(bass_path).apply_gain(bass_gain_db)
        mixed = song.overlay(bass)
        mixed.export(output_path, format="wav")
        print(f"[OK] Mixed audio → {output_path}")
    except Exception as e:
        print(f"[ERROR] Mix failed: {e}")
        raise e
