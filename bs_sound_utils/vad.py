import numpy as np
import webrtcvad

class VoiceActivityDetector:
    def __init__(self, sample_rate=16000, frame_duration_ms=30, padding_duration_ms=300, threshold=0.9):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.padding_duration_ms = padding_duration_ms
        self.threshold = threshold
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.vad = webrtcvad.Vad(1)  # 감도 설정 (0-3)
        self.reset()
    
    def reset(self):
        self.is_speech = False
        self.voiced_frames = []
        self.silent_frames = 0
        self.required_silent_frames = self.padding_duration_ms // self.frame_duration_ms
    
    def is_voiced(self, audio_frame):
        try:
            return self.vad.is_speech(audio_frame.tobytes(), self.sample_rate)
        except:
            return False
    
    def process_frame(self, audio_frame):
        is_voiced = self.is_voiced(audio_frame)
        
        if is_voiced:
            if not self.is_speech:
                self.is_speech = True
            self.silent_frames = 0
            self.voiced_frames.extend(audio_frame)
        else:
            if self.is_speech:
                self.silent_frames += 1
                self.voiced_frames.extend(audio_frame)
                
                if self.silent_frames >= self.required_silent_frames:
                    audio_data = np.array(self.voiced_frames)
                    self.reset()
                    return audio_data
        
        return None

if __name__ == "__main__":
    vad = VoiceActivityDetector()
    print(vad.process_frame(np.zeros(16000)))