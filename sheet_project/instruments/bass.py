from spleeter.separator import Separator
from pathlib import Path

def extract_bass(input_path: Path, output_path: Path):
    """
    🎸 Spleeter로 베이스 트랙만 추출
    """
    try:
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] Extracting bass from {input_path.name} ...")
        separator = Separator('spleeter:4stems')
        separator.separate_to_file(str(input_path), str(output_dir))

        # spleeter output/bass_project/bass/{filename}/bass.wav 형태로 저장됨
        result_path = output_dir / input_path.stem / "bass.wav"
        if not result_path.exists():
            raise FileNotFoundError("Bass track not found after separation")

        result_path.rename(output_path)
        print(f"[OK] Bass extracted → {output_path}")
    except Exception as e:
        print(f"[ERROR] Bass extraction failed: {e}")
        raise e
