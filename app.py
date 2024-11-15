import streamlit as st
import speech_recognition as sr
import requests
# Define the SpeechToText class
class SpeechToText:
    @staticmethod
    def print_mic():
        """Prints all available microphones."""
        mic_list = sr.Microphone.list_microphone_names()
        return mic_list

    @staticmethod
    def speech_to_text(device_index, language="vi-VN"):
        """Converts speech to text."""
        recognizer = sr.Recognizer()
        with sr.Microphone(device_index=device_index) as source:
            st.write("Recording...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=3)
            try:
                text = recognizer.recognize_google(audio, language=language)
                return text
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio."
            except sr.RequestError as e:
                return f"Google Speech Recognition error: {e}"

api_url = "https://khanhu2805-app--3000.prod1.defang.dev/post-control"
# Streamlit app layout
st.set_page_config(page_title='Nhận dạng giọng nói')
st.title("Nhận dạng giọng nói")

# Display available microphones
st.header("Thiết bị đang có")
mic_list = SpeechToText.print_mic()
if mic_list:
    for idx, mic_name in enumerate(mic_list):
        st.write(f"{idx}: {mic_name}")
else:
    st.write("Không tìm thấy thiết bị")

# Select microphone
device_index = st.number_input(
    "Nhập thiết bị thu âm:", min_value=0, max_value=len(mic_list) - 1, step=1
)

# Set language
language = st.selectbox("Lựa chọn ngôn ngữ:", ["vi-VN", "en-US", "fr-FR", "es-ES"])

# Start speech-to-text
if st.button("Thu âm"):
    if len(mic_list) > 0:
        result = SpeechToText.speech_to_text(device_index=device_index, language=language)
        st.write(f"Recognized Text: {result}")
        if (result == "bật đèn"):
            try:
                payload = {"value": "ohstem-yolobit-c99c", "action": "add"}
                response = requests.post(api_url, json=payload)
                st.write(f"Sent request: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.write(f"Error sending request: {e}")
        elif (result == "Tắt Đèn"):
            try:
                payload = {"value": "ohstem-yolobit-c99c", "action": "remove"}
                response = requests.post(api_url, json=payload)
                st.write(f"Sent request: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.write(f"Error sending request: {e}")

    else:
        st.write("Không tìm thấy thiết bị thu âm")
