# 실행 전 모듈 먼저 설치
# brew install portaudio && pip install pyaudio
# pip install openai
# pip install python-dotenv

import speech_recognition as sr
import pyaudio
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# https://platform.openai.com/account/api-keys
# Create new secret key 클릭해서 api key 생성
openai.api_key = os.environ.get('OPENAI_API_KEY')


def get_openai_response(prompt, print_output=False):

    completions = openai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=prompt,           # What the user typed in
        max_tokens=3072,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )
    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text


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

print("OpenAI GPT-3로 음성을 입력합니다. . . . .")
print("OpenAI GPT-3의 응답: " + get_openai_response(text))
