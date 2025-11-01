from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import traceback

# 모듈 import (AI, 오디오처리, 탭변환)
from instruments.bass import extract_bass
from services.tab_generator import generate_tab
from services.audio_mixer import mix_audio
from services.audio_player import get_audio_segment

# -------------------------------------------
# 🎵 기본 설정
# -------------------------------------------

app = FastAPI(title="Bass Tab Generator", version="1.0.0")

# Flutter와의 연결 허용 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 주요 폴더 경로 설정
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
for subfolder in ["bass", "mixed", "tabs"]:
    (OUTPUT_DIR / subfolder).mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------
# ✅ 헬스체크 (서버 상태 확인용)
# -------------------------------------------
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok", "message": "FastAPI server running"})

# -------------------------------------------
# 📤 1. 노래 업로드 + 베이스 추출 + Tab 생성
# -------------------------------------------
@app.post("/api/extract_bass")
async def extract_bass_api(file: UploadFile = File(...)):
    """
    클라이언트(Flutter)에서 노래 파일을 업로드하면:
    1️⃣ 파일 저장
    2️⃣ AI로 베이스 음원 추출
    3️⃣ Tab 악보 생성
    4️⃣ 결과 경로 반환
    """
    try:
        # 1️⃣ 파일 저장
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # 2️⃣ 베이스 트랙 추출
        bass_path = OUTPUT_DIR / "bass" / f"{file_id}_bass.wav"
        extract_bass(input_path, bass_path)  # instruments/bass.py

        # 3️⃣ Tab 악보 생성
        tab_path = OUTPUT_DIR / "tabs" / f"{file_id}_bass.txt"
        generate_tab(bass_path, tab_path)  # services/tab_generator.py

        # 4️⃣ 응답 반환
        return {
            "status": "success",
            "file_id": file_id,
            "original": str(input_path),
            "bass": str(bass_path),
            "tab": str(tab_path)
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------
# 🎧 2. 원곡 + 베이스 믹싱 (볼륨 조정)
# -------------------------------------------
@app.post("/api/mix_audio")
async def mix_audio_api(
    original: str = Form(...),
    bass: str = Form(...),
    bass_gain: float = Form(3.0)
):
    """
    두 오디오(원곡, 베이스)를 섞어 새로운 믹싱 음원을 만듦.
    bass_gain(dB): 베이스 음량을 조절
    """
    try:
        mixed_path = OUTPUT_DIR / "mixed" / f"mixed_{uuid.uuid4()}.wav"
        mix_audio(original, bass, mixed_path, bass_gain)
        return {"status": "success", "mixed": str(mixed_path)}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------
# ⏩ 3. 특정 위치부터 재생
# -------------------------------------------
@app.get("/api/play")
def play_segment(file_path: str, start_sec: float = 0.0):
    """
    오디오 파일을 특정 구간(start_sec)부터 재생.
    """
    try:
        segment_path = get_audio_segment(file_path, start_sec)
        return FileResponse(segment_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------
# 🎵 4. Tab 위치 데이터 반환
# -------------------------------------------
@app.get("/api/tab_positions/{file_id}")
def get_tab_positions(file_id: str):
    """
    특정 파일의 Tab 악보 내 시간-프렛 매핑 JSON 데이터 반환.
    (클릭 위치 재생용)
    """
    tab_json = OUTPUT_DIR / "tabs" / f"{file_id}_bass.json"
    if not tab_json.exists():
        raise HTTPException(status_code=404, detail="Tab JSON not found")
    return FileResponse(tab_json, media_type="application/json")


# -------------------------------------------
# 🏠 기본 페이지
# -------------------------------------------
@app.get("/")
def root():
    """
    정적 HTML 테스트 페이지 (optional)
    """
    html_path = BASE_DIR / "static" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return JSONResponse(content={"message": "Bass Tab Generator API is running"})
