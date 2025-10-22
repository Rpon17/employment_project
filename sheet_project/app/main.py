from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import subprocess, os, asyncio
from app.instruments.bass import extract_bass

# 앱 인스턴스 생성
app = FastAPI(title="Bass Transcriber API", version="1.0.0")

# Flutter 앱에서 접근 허용 (CORS 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ 배포 시엔 실제 앱 도메인으로 제한하기
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 출력 폴더 준비
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/health")
async def health_check():
    """서버 상태 확인용"""
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.post("/convert")
async def convert(
    youtube_url: str = Form(...),
    filename: str = Form(...)
):
    """
    🎵 유튜브 링크를 받아서:
    1️⃣ 오디오 다운로드 (yt-dlp)
    2️⃣ 베이스 분리 + MIDI 변환 (AI)
    3️⃣ 변환 결과를 JSON으로 반환
    """

    if not youtube_url.startswith("http"):
        raise HTTPException(status_code=400, detail="유효하지 않은 URL입니다.")

    # 안전한 파일명 처리
    safe_name = "".join(c for c in filename if c.isalnum() or c in ("-", "_"))
    output_wav = OUTPUT_DIR / f"{safe_name}.wav"

    # 1️⃣ 유튜브 오디오 다운로드
    cmd = [
        "yt-dlp", "-x", "--audio-format", "wav",
        youtube_url, "-o", str(output_wav)
    ]
    try:
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오디오 다운로드 실패: {e}")

    # 2️⃣ 베이스 추출 및 MIDI 변환
    try:
        midi_file = extract_bass(
            input_file=str(output_wav),
            output_dir=str(OUTPUT_DIR)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 변환 실패: {e}")

    # 3️⃣ 결과 JSON 반환 (Flutter가 받아서 표시)
    midi_filename = os.path.basename(midi_file)
    return JSONResponse(
        content={
            "status": "success",
            "filename": midi_filename,
            "midi_path": f"/files/{midi_filename}",
            # 추후 AWS S3 업로드 시 presigned URL로 교체 예정
        },
        status_code=200
    )
