import configparser, sys
from transformers import WhisperProcessor, WhisperForConditionalGeneration

config = configparser.ConfigParser()
config.read('/bssoft/config.ini')

sys.path.insert(1, config['dirs']['ml_path'])

stt_model_path = "openai/whisper-medium"

if config['ml']['device'] == 'gpu':
    device = 'cuda:1'
else :
    device = 'cpu'

models = {}
# stt_model = WhisperForConditionalGeneration.from_pretrained(stt_model_path)

stt_processors = {}
stt_processors['processor'] = WhisperProcessor.from_pretrained(stt_model_path)
#stt_processors['forced_decoder_ids'] = stt_processors['processor'].get_decoder_prompt_ids(language="korean", task="transcribe")
models['stt_model'] = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").to(device)
models['stt_model'].config.forced_decoder_ids = stt_processors['processor'].tokenizer.get_decoder_prompt_ids(language="korean", task="transcribe")