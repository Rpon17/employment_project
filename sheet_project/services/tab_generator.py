import librosa
import numpy as np
from pathlib import Path
import json

STRING_BASE_FREQ = {"E": 41.20, "A": 55.00, "D": 73.42, "G": 98.00}

def freq_to_note(freq):
    if freq <= 0:
        return None
    return int(np.round(69 + 12 * np.log2(freq / 440.0)))

def generate_tab(bass_path: Path, tab_output: Path):
    try:
        print(f"[INFO] Generating TAB from {bass_path}")
        y, sr = librosa.load(bass_path, sr=22050)
        f0, _, _ = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("E2"),
            fmax=librosa.note_to_hz("C5"),
        )
        times = librosa.times_like(f0, sr=sr)

        tab_lines = {"E": [], "A": [], "D": [], "G": []}
        tab_data = []

        for t, freq in zip(times, f0):
            if freq is None:
                continue
            closest_string, closest_fret, min_diff = None, None, 9999
            for string, base_freq in STRING_BASE_FREQ.items():
                fret = 12 * np.log2(freq / base_freq)
                if 0 <= fret <= 20:
                    diff = abs(freq - base_freq * (2 ** (fret / 12)))
                    if diff < min_diff:
                        min_diff, closest_string, closest_fret = diff, string, round(fret)
            if closest_string:
                tab_lines[closest_string].append((t, closest_fret))
                tab_data.append({
                    "time": float(t),
                    "string": closest_string,
                    "fret": int(closest_fret),
                })

        # TXT 탭 생성
        txt = []
        for s in ["G", "D", "A", "E"]:
            line = f"{s}|"
            for _, f in tab_lines[s]:
                line += f"--{f:02d}--"
            txt.append(line + "|")
        with open(tab_output, "w") as f:
            f.write("\n".join(txt))

        # JSON 저장 (시간-프렛 매핑)
        json_path = tab_output.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(tab_data, jf, indent=2)
        print(f"[OK] Tab generated → {tab_output}")
    except Exception as e:
        print(f"[ERROR] Tab generation failed: {e}")
        raise e
