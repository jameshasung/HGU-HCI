import os
import speech_recognition as sr
import pyaudio
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Flask 애플리케이션 생성
app = Flask(__name__)

# OpenAI API Key 설정
openai.api_key = os.environ.get('OPENAI_API_KEY')

# OpenAI GPT-3로 응답 생성


def get_openai_response(prompt, print_output=False):
    completions = openai.Completion.create(
        engine='text-davinci-003',
        temperature=0.5,
        prompt=prompt,
        max_tokens=3072,
        n=1,
        stop=None,
    )
    if print_output:
        print(completions)
    return completions.choices[0].text

# 음성 입력을 텍스트로 변환하는 함수


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("음성을 입력하세요.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ko-KR')
        print("인식된 텍스트: " + text)
        return text
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        return None
    except sr.RequestError as e:
        print("구글 음성 인식 API에 접근할 수 없습니다: {0}".format(e))
        return None

# Flask 라우트 및 뷰 함수


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_openai_response', methods=['POST'])
def get_response():
    if request.method == 'POST':
        text = request.form['text']
        response = get_openai_response(text)
        return response


@app.route('/speech_to_text', methods=['GET'])
def speech_to_text():
    text = recognize_speech()
    if text is not None:
        return text
    else:
        return "음성 인식에 실패했습니다."


if __name__ == '__main__':
    app.run()
