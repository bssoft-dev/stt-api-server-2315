import numpy as np
import queue
import torch
import warnings
from utils.sys import aprint
from bs_sound_utils.vad import VoiceActivityDetector
warnings.filterwarnings("ignore")

class RealtimeSTT:
    def __init__(self, processor, model, language="ko"):
        self.rooms = {}
        self.processor = processor
        self.model = model
        self.language = language
        if torch.cuda.is_available():
            self.device = "cuda:1"
        #     self.model = self.model.to(self.device)
        else:
            self.device = "cpu"
        # 오디오 설정
        self.sample_rate = 16000
        self.frame_duration_ms = 30 # only can be 10, 20, 30
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)
        # VAD 설정
        self.vad_detector = VoiceActivityDetector(
            sample_rate=self.sample_rate,
            frame_duration_ms=self.frame_duration_ms
        )
    
    def get_room_names(self):
        return list(self.rooms.keys())
    
    def add_room(self, room_name: str):
        self.rooms[room_name] = queue.Queue()
        
    def run(self, audio_data: np.ndarray, room_name: str): # 형식 - np.int16, 16000, 1ch
        self.process_vad(audio_data, room_name)
        result = None
        if not self.rooms[room_name].empty():
            result = self.transcribe_audio(room_name)
        return result
        
    def process_vad(self, audio_data: np.ndarray, room_name: str):
        """오디오 처리 및 VAD 적용"""
        try:
            # 프레임 단위로 처리
            for i in range(0, len(audio_data), self.frame_size):
                frame = audio_data[i:i + self.frame_size]
                if len(frame) == self.frame_size:
                    result = self.vad_detector.process_frame(frame)
                    if result is not None and len(result) > self.frame_size * 3:  # 최소 길이 체크
                        self.rooms[room_name].put(result)
        except Exception as e:
            print(f"오디오 처리 중 에러 발생: {str(e)}")
                    
    def transcribe_audio(self, room_name: str):
        """음성을 텍스트로 변환"""
        try:
            audio_data = self.rooms[room_name].get(timeout=1)
            # float32로 변환
            audio_data = audio_data.astype(np.float32) / 32767.0
            # 입력 특성 생성
            input_features = self.processor(
                audio_data, 
                sampling_rate=self.sample_rate, 
                return_tensors="pt"
            ).input_features
            input_features = input_features.to(self.device)
            # Whisper 모델로 음성 인식
            predicted_ids = self.model.generate(
                input_features,
                language=self.language,
                task="transcribe"
            )
            # 텍스트 변환
            transcription = self.processor.batch_decode(
                predicted_ids, 
                skip_special_tokens=True
            )[0]
            if transcription.strip():
                aprint(f"인식된 텍스트: {transcription}")
                result = transcription
        except Exception as e:
            print(f"텍스트 변환 중 에러 발생: {str(e)}")
                
        return result