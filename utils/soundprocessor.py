import torch, librosa

def predict(processors: dict, model, sr, wav_data):
    tmp = processors['processor'](wav_data, sampling_rate = sr, return_tensors='pt')
    input_values = tmp.input_features.to('cuda')
    with torch.no_grad():
        generated_ids = model.generate(input_values)
    pred = processors['processor'].batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(pred)
    return pred

def stt(filepath: str, processors: dict, model, thres = 0.3, sr = 16000):
    wav_data = librosa.load(filepath, sr=sr)[0]
    sentence = ''
    if len(wav_data) / sr > 30:
        for i in range(0, len(wav_data), sr*30):
            pred = predict(processors, model, sr, wav_data[i:i+sr*30])
            sentence = sentence + pred
    else:
        sentence = predict(processors, model, sr, wav_data)
    return sentence