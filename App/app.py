import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import base64
import time
import pygame
import io
from gtts import gTTS
from flask import Flask, request, jsonify
from threading import Thread

# تكوين API الخاص بـ Google Generative AI
genai.configure(api_key='your_ApI')

app = Flask(__name__)

# صفحة HTML الرئيسية
@app.route('/')
def index():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

# API لاستقبال الرسائل من واجهة المستخدم
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response = get_chat_response(user_message)
    return jsonify({"response": response})

def recognize_speech_from_mic(language):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

pygame.mixer.init()

def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    output = io.BytesIO()
    tts.write_to_fp(output)
    output.seek(0)
    pygame.mixer.music.load(output)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_chat_response(question):
    info = '''
    Chatbot Info
    "Your name is Chatbota"
    "You are a female"
    "You're built with Gemimi 1.5 pro model"

    Chatbot Creator Info
    "Barah Qusai, 22 years old and Data Scientist."
    "Phone number: +249115791992"
    "Email: Barah Qusai@gmail.com"

    Greeting
    "Hello!"
    "Hi there, how can I help?"
    "May the peace, blessings, and mercy of God be upon you"

    Goodbye
    "Sad to see you go :("
    "Talk to you later"
    "Goodbye!"

    Course Info
    "We offer a wide range of courses in various subjects including technology, business, arts, and more. Some of our popular courses include 'Introduction to Python Programming,' 'Digital Marketing Essentials,' 'Graphic Design Fundamentals,' and 'Project Management Professional (PMP) Certification.' You can explore our full course catalog on our website."

    Enrollment
    "To enroll in a course, simply visit our website, browse through the available courses, and click on the 'Enroll Now' button for the course you're interested in. For example, if you want to enroll in 'Advanced Excel for Business,' just find the course and follow the instructions to complete the enrollment process."

    Payment
    "We offer various payment options including credit/debit card, PayPal, and bank transfer. Some courses may have a fee while others might be free. For instance, 'Basic Web Development' is free, while 'Data Science with R' has a fee. You can find detailed payment information on the course page."

    Refund
    "We have a refund policy in place for cases where students are not satisfied with the course. You can request a refund within a certain period after enrolling in the course. For example, if you're not satisfied with 'Creative Writing,' you can request a refund within the stipulated time. Please refer to our refund policy page on our website for more details."

    Technical Support
    "If you're experiencing technical issues with our website, please reach out to our technical support team at support@website.com. They'll be happy to assist you with any problems you're encountering, whether it's with 'Introduction to Cybersecurity' or any other course."

    Course Recommendation
    "Could you please provide me with some information about your interests or the subject you're interested in learning? For example, if you're interested in technology, I might recommend 'Full Stack Web Development,' but if you're into business, 'Entrepreneurship 101' could be a great choice."

    Course Duration
    "The duration of our courses varies depending on the subject and level. For example, 'Beginner's Guide to Photography' is a 4-week course, while 'Advanced Machine Learning' lasts for 12 weeks. You can find the duration information on the course details page when you enroll."

    Certificate
    "Upon successful completion of a course, you will receive a certificate. This certificate can be a valuable addition to your resume or LinkedIn profile. Courses like 'Certified Ethical Hacker' and 'Financial Analysis for Managers' provide certificates upon completion."

    Course Schedule
    "Course start dates vary depending on the course. For example, 'Introduction to Java' might start every month, while 'Marketing Analytics' might have a quarterly start date. You can check the course schedule on our website or contact our support team for more information."

    Prerequisites
    "Some of our courses may have prerequisites or recommended background knowledge. For instance, 'Advanced Data Structures' requires prior knowledge of basic programming. You can find information about prerequisites on the course details page."
    '''
    prompt = f"Question: {question}. Respond to this question only based on the Info provided below and respond only in Arabic or English based on Question language. Info: {info}."
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

def run_flask():
    app.run(port=5000, debug=False)

flask_thread = Thread(target=run_flask)
flask_thread.start()

# جزء Streamlit
st.title("Chatbota for Courses Website")

if "language" not in st.session_state:
    st.session_state.language = "ar"

if "show_conversation" not in st.session_state:
    st.session_state.show_conversation = False

if st.button("Speak"):
    recognized_text = recognize_speech_from_mic(st.session_state.language)
    if recognized_text:
        st.session_state.messages.append({"role": "user", "content": recognized_text})

st.session_state.language = st.radio("Select Language:", ('ar', 'en'), format_func=lambda x: "Arabic (العربية)" if x == 'ar' else "English")

if st.button("Show/Hide Conversation"):
    st.session_state.show_conversation = not st.session_state.show_conversation

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.show_conversation:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if "recognized_text" in locals():
    if st.session_state.show_conversation:
        with st.chat_message("user"):
            st.markdown(recognized_text)
        with st.chat_message("assistant"):
            response = get_chat_response(recognized_text)
            st.markdown(response)
    else:
        response = get_chat_response(recognized_text)

    st.session_state.messages.append({"role": "assistant", "content": response})
    text_to_speech(response, st.session_state.language)