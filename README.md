# Chatbut-with-Gemini-

This chatbot has several features that make it effective and appealing to use, including:

1. **Attractive and Modern User Interface**:
    - A dark mode design that makes the interface easy on the eyes, especially in low-light conditions.
    - Animation effects that add liveliness to the interface and make it more engaging.

2. **Support for Text, Voice, and Images**:
    - Ability to receive text inputs from users via an input field.
    - Voice recording feature that allows users to speak directly to the chatbot and convert voice to text using speech recognition.
    - Option to upload images for interaction with the chatbot.

3. **Knowledge-Based Responses**:
    - The chatbot answers questions based on a predefined set of information related to courses and services offered, ensuring accurate and relevant responses.

4. **Integration with Google Generative AI**:
    - Utilizes an advanced model from Google Generative AI to ensure high-quality and fast responses, providing a natural and smooth conversation experience.

5. **Text-to-Speech Conversion**:
    - Uses the gTTS library to convert text responses into audio that users can listen to, enhancing accessibility and user experience.

6. **Conversation Storage**:
    - Saves conversations between the user and the chatbot for later review, allowing users to easily revisit previous dialogues.

7. **Multilingual Support**:
    - Ability to choose the language (Arabic or English), enabling broader communication with a larger user base.

### Technical Details:
- **Flask**: Used to provide APIs and serve the HTML page.
- **Streamlit**: Used to build an interactive and user-friendly interface, convert text to speech, and receive user inputs.
- **Threading**: Ensures that both Flask and Streamlit run simultaneously.
- **Speech Recognition**: Uses the `speech_recognition` library to convert speech to text.
- **Google Generative AI Model**: Generates intelligent and contextually appropriate responses.
