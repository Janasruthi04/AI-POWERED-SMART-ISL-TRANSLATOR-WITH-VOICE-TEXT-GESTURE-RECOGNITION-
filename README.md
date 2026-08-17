# 🌐 Smart ISL Translator with Voice, Text & Gesture Recognition

An AI-powered multilingual translator that converts **text, speech, and words into sign language gestures**, with additional features like **text-to-speech, live language learning, and custom vocabulary building**.

---

## 🚀 Features

### 🔤 Text Translation
- Translate text between multiple languages
- Supports: English, French, Spanish, German, Hindi, Telugu, Tamil

### 🎤 Speech-to-Text Translation
- Upload audio files and convert speech → text → translation

### 🎙️ Live Audio Recording
- Record voice directly and translate in real-time

### 🔊 Text-to-Speech (TTS)
- Converts translated text into natural audio output

### 🤖 AI Language Teacher
- Interactive chatbot for language learning
- Provides:
  - Meaning
  - Pronunciation
  - Example sentence

### 📚 Custom Vocabulary
- Add and store your own words
- Includes meaning, example, and translation

### ✋ Words to Sign Language Gestures
- Converts text into sign language alphabets (A–Z)
- Supports multiple sign languages:
  - American (ASL)
  - British (BSL)
  - Australian (AusSL)
  - Chinese (CSL)
  - French (FSL)
  - Spanish (LSE)

---

## 🛠️ Tech Stack

- **Frontend/UI:** Gradio  
- **Speech Recognition:** AssemblyAI  
- **Translation:** translate (Python library)  
- **Text-to-Speech:** gTTS  
- **AI Chatbot:** Google Gemini API  
- **Image Processing:** Pillow  

---

## 📁 Project Structure


project/
│
├── main.py
├── custom_vocab.json
│
├── gestures/
│ ├── ASL/
│ ├── BSL/
│ ├── AusSL/
│ ├── CSL/
│ ├── FSL/
│ └── LSE/
│
└── generated_audio_files/


---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-link>
cd project
2️⃣ Install Dependencies
pip install gradio assemblyai translate gtts google-generativeai pillow
🔑 API Setup
AssemblyAI
Replace with your API key:
aai.settings.api_key = "YOUR_API_KEY"
Google Gemini
genai.configure(api_key="YOUR_API_KEY")

pip install -r requirements.txt

▶️ Run the Application
python translator.py

Then open in browser:
http://127.0.0.1:7861