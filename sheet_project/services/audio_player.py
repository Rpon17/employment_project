from pydub import AudioSegment
from pathlib import Path

def get_audio_segment(file_path: str, start_sec: float = 0.0, duration: float = 10.0):
    """
    🎧 특정 시점(start_sec)부터 일정 구간(duration초)을 잘라낸 오디오 파일을 반환
    """
    try:
        audio = AudioSegment.from_file(file_path)
        start_ms = start_sec * 1000
        end_ms = min(len(audio), start_ms + (duration * 1000))
        segment = audio[start_ms:end_ms]

        temp_path = Path("output/temp_segment.wav")
        segment.export(temp_path, format="wav")
        print(f"[OK] Segment exported → {temp_path}")
        return temp_path
    except Exception as e:
        print(f"[ERROR] Segment extraction failed: {e}")
        raise e
