# 실행 전 모듈 먼저 설치
# (mac)brew install portaudio && pip install pyaudio

import speech_recognition as sr
import pyaudio

# 음성 입력 설정
r = sr.Recognizer()
with sr.Microphone() as source:
    print("음성을 입력하세요.")
    audio = r.listen(source)

# 음성을 텍스트로 변환
try:
    text = r.recognize_google(audio, language='ko-KR')  # 구글 음성 인식 API 사용
    print("인식된 텍스트: " + text)
except sr.UnknownValueError:
    print("음성을 인식할 수 없습니다.")
except sr.RequestError as e:
    print("구글 음성 인식 API에 접근할 수 없습니다: {0}".format(e))
