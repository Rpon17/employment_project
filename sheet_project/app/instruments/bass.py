import os
from pathlib import Path

def extract_bass(input_file: str, output_dir: str) -> str:
    """
    🎵 베이스 음 추출 및 MIDI 변환 (임시 버전)
    실제 AI 모델이 완성되면 이 함수 안에서 오디오 -> 베이스 -> MIDI 변환 수행.
    
    Args:
        input_file (str): 입력 WAV 파일 경로
        output_dir (str): 출력 폴더 경로

    Returns:
        str: 생성된 MIDI 파일 경로
    """

    # 출력 폴더 확인
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    # 입력 파일명 기반으로 MIDI 파일 이름 생성
    base_name = Path(input_file).stem
    midi_path = output_path / f"{base_name}.mid"

    # 지금은 더미 데이터로 대체 — 실제론 추출된 MIDI를 저장해야 함
    with open(midi_path, "w", encoding="utf-8") as f:
        f.write(f"0 0 NoteOn C3 80\n0 480 NoteOff C3 0\n")
        f.write(f"0 480 NoteOn E3 80\n0 960 NoteOff E3 0\n")

    print(f"[INFO] Bass line dummy MIDI generated → {midi_path}")
    return str(midi_path)
