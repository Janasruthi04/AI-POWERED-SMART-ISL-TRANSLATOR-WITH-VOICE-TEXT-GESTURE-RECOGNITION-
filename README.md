# AI-POWERED-SMART-ISL-TRANSLATOR-WITH-VOICE-TEXT-GESTURE-RECOGNITION-
An AI-powered multilingual communication and learning application designed to help bridge communication barriers for users who depend on Indian Sign Language or face speech/hearing limitations.
The system combines Speech-to-Text, Text-to-Speech, multilingual translation, conversational AI, custom vocabulary management, and words-to-gesture visualization into a unified Gradio-based application.

🚀 Key Features
🎙️ Speech-to-Text (ASR) – Converts uploaded or recorded speech into text using AssemblyAI.
🌐 Multilingual Translation – Translates text between supported languages using chunk-based translation.
🔊 Text-to-Speech (TTS) – Converts translated text into speech using gTTS.
🤖 Conversational AI – Uses Google Gemini to provide AI-supported language practice and conversational tutoring.
📚 Custom Vocabulary – Stores domain-specific words, meanings, usage, and translations using a JSON-based vocabulary system.
🤟 Words-to-Gestures – Maps alphabetic characters to sign-language gesture images to support sign-language learning.
🖥️ Interactive Interface – Provides an integrated Gradio interface for text, audio, translation, and learning workflows.
🔄 Multimodal Workflow – Supports typed text, uploaded audio, and recorded speech as inputs.
🧠 Technologies Used

Programming:
Python

AI / NLP:
Natural Language Processing, Conversational AI, Google Gemini

Speech & Audio:
AssemblyAI, Speech-to-Text (ASR), Text-to-Speech (TTS), Audio Processing

Translation:
Python Translate Library

Text-to-Speech:
gTTS

Frontend / Application:
Gradio

Data & Storage:
JSON-based Custom Vocabulary

System Workflow
Text Input ───────────────┐
                          │
Audio / Recorded Speech ──┤
                          ↓
                  Speech-to-Text
                    (AssemblyAI)
                          ↓
                Multilingual Translation
                          ↓
             ┌────────────┴────────────┐
             ↓                         ↓
       Text Output                Text-to-Speech
                                         ↓
                                  Audio Output


                    ┌─────────────────┐
                    ↓                 ↓
              Gemini AI          Custom Vocabulary
           Conversational AI       Management


                    ↓
             Words-to-Gestures
              Sign Visualization

Project Objectives
Enable accessible communication through text and speech.
Support multilingual translation and speech output.
Provide conversational AI-based language practice.
Maintain reusable vocabulary for personalized learning.
Provide basic sign-linked educational support through gesture visualization.
Integrate multiple AI-powered communication capabilities into a single application.
