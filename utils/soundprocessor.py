import torch, librosa

def stt(filepath: str, processors: dict, model, thres = 0.3, sr = 16000):
    wav_data = librosa.load(filepath, sr=sr)[0]
    tmp = processors['processor'](wav_data, sampling_rate = sr, return_tensors='pt')
    input_values = tmp.input_features.to('cuda')
    with torch.no_grad():
        # generated_ids = model.generate(input_values, forced_decoder_ids=processors['forced_decoder_ids'])
        generated_ids = model.generate(input_values)
    pred = processors['processor'].batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(pred)
    return pred