import uvicorn, os, shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from lnp.vocabraries import filter_forbidden
from utils.soundprocessor import stt
from utils.webSocket import notifier
from routers import webSocketClient
from utils.ini import (config, models, stt_processors)
from utils.log_conf import app_log_conf

app = FastAPI(
    title="STT 기몬모델 API 서버",
    description="STT 테스트 서버입니다."
)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(webSocketClient.router)

BASE_DIR=config['dirs']['upload_path']
STT_DIR=config['dirs']['stt_path']


@app.get("/")
async def root():
    return {"message": "BSsoft STT Model Server API is running"}

@app.post("/analysis/stt/wavfile")
async def stt_anal(file: UploadFile = File(...)):
    '''
    wav 파일 업로드 기반 STT
    '''
    if "wav" not in file.filename[-3:]:
        raise HTTPException(status_code=422, detail="File extension is not allowed")
    folder = os.path.join(BASE_DIR, 'stt')
    soundfile = os.path.join(folder,file.filename)
    with open(soundfile, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    res = stt(soundfile, stt_processors, models['stt_model'])
    res = filter_forbidden(res)
    return {"file": file.filename, "result": res}



# WebSocket 연결을 위한 라우트 추가
@app.websocket("/ws/byte")
async def websocket_endpoint2(websocket: WebSocket):
    '''
    녹음된 음원 byte 전송 기반 STT 기본 모델 테스트
    '''
    await notifier.connect(websocket)
    count = 0
    try:
        while True:
            data = await websocket.receive_bytes()
            soundfile = os.path.join(STT_DIR, f'{count}.wav')
            with open(soundfile, "wb") as buffer:
                buffer.write(data)
            res = stt(soundfile, stt_processors, models['stt_model'])
            res = filter_forbidden(res)
            # response_data = {"data": res}  # 응답할 데이터를 딕셔너리 형태로 구성
            # print(res)

            await websocket.send_json(res)  # JSON 응답 전송
            # await notifier.push(response_data)
            if count < 20:
                count += 1
            else:
                count = 0
    except WebSocketDisconnect:
        notifier.remove(websocket)

if __name__ == '__main__':
    uvicorn.run("app:app", host=config['host']['url'], port=int(config['host']['port']), reload=True,
                log_config=app_log_conf, log_level='info')
