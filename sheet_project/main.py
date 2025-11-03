from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import traceback

# 내부 모듈 import
from instruments.bass import extract_bass
from services.tab_generator import generate_tab
from services.audio_mixer import mix_audio
from services.audio_player import get_audio_segment

app = FastAPI(title="Bass Tab Generator", version="1.0.0")

# 🌐 Flutter / 웹 연결 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
for sub in ["bass", "mixed", "tabs"]:
    (OUTPUT_DIR / sub).mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ✅ 헬스체크
@app.get("/health")
def health():
    return {"status": "ok"}

# 🎵 1. 노래 업로드 → 베이스 추출 → 탭 생성
@app.post("/api/extract_bass")
async def extract_bass_api(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
        with open(input_path, "wb") as f:
            f.write(await file.read())

        bass_path = OUTPUT_DIR / "bass" / f"{file_id}_bass.wav"
        extract_bass(input_path, bass_path)

        tab_path = OUTPUT_DIR / "tabs" / f"{file_id}_bass.txt"
        generate_tab(bass_path, tab_path)

        return {
            "status": "success",
            "file_id": file_id,
            "original": str(input_path),
            "bass": str(bass_path),
            "tab": str(tab_path),
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 🎚️ 2. 원곡 + 베이스 믹싱
@app.post("/api/mix_audio")
async def mix_audio_api(
    original: str = Form(...),
    bass: str = Form(...),
    bass_gain: float = Form(3.0)
):
    try:
        mixed_path = OUTPUT_DIR / "mixed" / f"mixed_{uuid.uuid4()}.wav"
        mix_audio(original, bass, mixed_path, bass_gain)
        return {"mixed": str(mixed_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ⏩ 3. 특정 구간 재생
@app.get("/api/play")
def play_segment(file_path: str, start_sec: float = 0.0):
    try:
        segment_path = get_audio_segment(file_path, start_sec)
        return FileResponse(segment_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def home():
    return {"message": "FastAPI server running 🚀"}
