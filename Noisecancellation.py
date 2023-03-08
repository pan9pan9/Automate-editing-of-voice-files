import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# 음성 파일 불러오기
audio_path = "sample.wav"
y, sr = librosa.load(audio_path)

# 음성 파일에서 진폭이 0.1 이하인 값을 0으로 만들기
thresh = 0.05

mute_times = []

# 진폭이 threshold 이하인 구간을 검사하여 mute 시간을 구함
is_muted = False
mute_start = 0
for i in range(len(y)):
    if np.abs(y[i]) < thresh:
        if not is_muted:
            mute_start = i
            is_muted = True
    else:
        if is_muted:
            mute_end = i
            mute_duration = librosa.samples_to_time(mute_end - mute_start, sr=sr)
            if mute_duration >= 0.5:  # mute 기준 시간 설정 (예: 0.5초 이상)
                mute_times.append((mute_start, mute_end))
            is_muted = False

# mute 시간에 해당하는 구간을 0으로 대체
for mute_start, mute_end in mute_times:
    y[mute_start:mute_end] = 0

output_path = 'result1.wav'

sf.write(output_path, y, sr)

# 음성 파일의 파형 시각화
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y, sr=sr)
plt.title('Muted audio waveplot')
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()

