import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import speech_recognition as sr
from pydub import AudioSegment

# 음성 파일 불러오기
audio_path = "sample.wav"
y, sd = librosa.load(audio_path)

# 음성 파일에서 진폭이 0.1 이하인 값을 0으로 만들기
thresh = 0.1

# mute 구간의 길이와 시간을 지정
mute_length = 0.1 # mute 구간 길이 (초)
mute_time = librosa.time_to_samples(mute_length, sr=sd)  # mute 구간 시간 (샘플)

# mute 처리할 구간을 저장하는 리스트
mute_ranges = []

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
            mute_duration = librosa.samples_to_time(mute_end - mute_start, sr=sd)
            if mute_duration >= 0.4:  # mute 기준 시간 설정
                mute_ranges.append((mute_start, mute_end))
            is_muted = False

# mute 시간에 해당하는 구간을 0으로 대체
for mute_start, mute_end in mute_ranges:
    y[mute_start+mute_time:mute_end-mute_time] = 0

output_path = 'result.wav'

sf.write(output_path, y, sd)

# 음성 파일의 파형 시각화

"""
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y, sr=sd)
plt.title('Muted audio waveplot')
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
"""

#음성인식 으로 추출 (실패)
"""
r = sr.Recognizer()

# 음성 파일 읽기
with sr.AudioFile(output_path) as source:
    audio = r.record(source)

# 음성인식
text = r.recognize_google(audio, language="ko-KR")

# 주어진 텍스트 추출
target_text = "안녕하세요 런데이입니다"
index = text.find(target_text)


if index != -1:

    # 오디오 파일 로드
    audio = AudioSegment.from_file(output_path)

    # 오디오 파일을 numpy 배열로 변환
    audio_array = np.array(audio.get_array_of_samples())

    # 주어진 텍스트 위치에서 음성 신호 추출
    frame_length = int(0.5 * sd)  # 음성 신호 길이 1초
    hop_length = int(0.1 * sd)  # 음성 신호 겹치는 구간 0.5초
    start = max(0, librosa.time_to_samples(librosa.samples_to_time(index/sd) - 0.5, sr=sd))
    end = librosa.time_to_samples(librosa.samples_to_time(index/sd) + len(target_text)/sd + 0.5, sr=sd)
    extracted_audio, _ = librosa.effects.trim(audio_array[start:end], top_db=20, frame_length=frame_length, hop_length=hop_length)

extracted_path = "extracted_audio.wav"
sf.write(extracted_path, extracted_audio, sd)
"""