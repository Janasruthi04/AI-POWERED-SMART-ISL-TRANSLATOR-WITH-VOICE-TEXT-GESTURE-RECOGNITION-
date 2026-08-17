import asyncio
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import gradio as gr
import assemblyai as aai
from translate import Translator
from gtts import gTTS
import uuid
from pathlib import Path
import textwrap
import google.generativeai as genai
import json
from PIL import Image

# -----------------------------
# WINDOWS PYTHON 3.12 FIX
# -----------------------------
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ================== GEMINI ==================
genai.configure(api_key="AIzaSyBrGzi0_DrBsFmt8kEbpcaPni-AMuQTdhU")
gemini_model = genai.GenerativeModel("models/gemini-flash-latest")

# ================= CUSTOM VOCABULARY =================
VOCAB_FILE = "custom_vocab.json"

def load_vocab():
    try:
        with open(VOCAB_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def add_vocab(word, meaning, example, translation):
    vocab = load_vocab()
    vocab[word] = {"meaning":meaning,"example":example,"translation":translation}
    with open(VOCAB_FILE,"w",encoding="utf-8") as f:
        json.dump(vocab,f,indent=2,ensure_ascii=False)
    return f"✅ '{word}' added!"

def show_vocab():
    vocab = load_vocab()
    if not vocab:
        return "📂 Vocabulary empty"
    out="### Custom Vocabulary\n"
    for w,d in vocab.items():
        out += f"**{w}** → {d['meaning']}  \n"
        out += f"Example: {d['example']}  \n"
        out += f"Translation: {d['translation']}  \n\n"
    return out

# ================= TRANSLATION =================
def transcribe_audio(audio_file):
    aai.settings.api_key = "595c181bb2e8460a8a1745df7f803089"
    return aai.Transcriber().transcribe(audio_file)

def translate_text(text, from_lang="English", to_lang="French"):
    lang_map={
        "English":"en","French":"fr","Spanish":"es","German":"de",
        "Hindi":"hi","Telugu":"te","Tamil":"ta"
    }

    translator = Translator(
        from_lang=lang_map.get(from_lang,"en"),
        to_lang=lang_map.get(to_lang,"fr")
    )

    chunks=textwrap.wrap(text,width=500)
    res=[]
    for c in chunks:
        try:
            res.append(translator.translate(c))
        except Exception as e:
            res.append(str(e))
    return " ".join(res)

# ================= TTS =================
LANGUAGE_CODES={
    "English":"en","French":"fr","Spanish":"es",
    "German":"de","Hindi":"hi","Telugu":"te","Tamil":"ta"
}

def text_to_speech(text,lang="English"):
    tts=gTTS(text=text,lang=LANGUAGE_CODES.get(lang,"en"))
    fname=f"{uuid.uuid4()}.mp3"
    tts.save(fname)
    return fname

def translate_and_generate(text,input_lang,target_lang):
    translated=translate_text(text,input_lang,target_lang)
    audio=text_to_speech(translated,target_lang)
    return Path(audio), translated

def process_input(text_input,audio_file,recorded_audio,input_lang,target_lang):

    if text_input:
        return translate_and_generate(text_input,input_lang,target_lang)
    elif audio_file:
        transcript=transcribe_audio(audio_file)
    elif recorded_audio:
        transcript=transcribe_audio(recorded_audio)
    else:
        raise gr.Error("Provide text or audio")

    if getattr(transcript,"error",None):
        raise gr.Error(transcript.error)

    return translate_and_generate(transcript.text,input_lang,target_lang)

# ================= LANGUAGE TEACHER =================
def language_teacher(msg,lang,history):
    if not msg.strip():
        return history,""

    prompt=f"""
You are a friendly language tutor.
User learning: {lang}

Reply in {lang}
Give English meaning
Give pronunciation
Give one example sentence

User: {msg}
"""
    reply=gemini_model.generate_content(prompt).text
    history.append({"role":"user","content":msg})
    history.append({"role":"assistant","content":reply})
    return history,""

# ================= WORDS TO GESTURES =================

ASL_MAP={chr(i):f"{chr(i).lower()}.webp" for i in range(65,91)}
BSL_MAP={chr(i):f"b{chr(i).lower()}.webp" for i in range(65,91)}
CSL_MAP={chr(i):f"c{chr(i).lower()}.webp" for i in range(65,91)}
FSL_MAP={chr(i):f"f{chr(i).lower()}.webp" for i in range(65,91)}
LSE_MAP={chr(i):f"s{chr(i).lower()}.webp" for i in range(65,91)}

LANGUAGE_GESTURE_CONFIG={
    "American": ("gestures/ASL", ASL_MAP),
    "British": ("gestures/BSL", BSL_MAP),
    "Australian": ("gestures/AusSL", BSL_MAP),
    "Chinese": ("gestures/CSL", CSL_MAP),
    "French": ("gestures/FSL", FSL_MAP),
    "Spanish": ("gestures/LSE", LSE_MAP)
}

def resize_image(img,size=140):
    canvas=Image.new("RGB",(size,size),"white")
    img.thumbnail((size,size))
    canvas.paste(img,((size-img.width)//2,(size-img.height)//2))
    return canvas

def words_to_gestures(text,language="American"):
    folder,cmap=LANGUAGE_GESTURE_CONFIG.get(
        language, LANGUAGE_GESTURE_CONFIG["American"]
    )
    out=[]
    for ch in text.upper():
        if ch in cmap:
            path=os.path.join(folder,cmap[ch])
            if os.path.exists(path):
                img=resize_image(Image.open(path).convert("RGB"))
                out.append((img,ch))
    return out

# ====================== UI ======================
with gr.Blocks(css=".gallery img{object-fit:contain;background:white;}") as demo:

    gr.Markdown("<h1 style='text-align:center;color:#6c63ff;'>Smart ISL Translator with Voice, Text & Gesture Recognition</h1>")

    with gr.Tabs():

        with gr.Tab("Text Input"):
            input_lang=gr.Dropdown(list(LANGUAGE_CODES.keys()),value="English")
            target_lang=gr.Dropdown(list(LANGUAGE_CODES.keys()),value="French")
            text_input=gr.Textbox(label="Enter Text")
            btn=gr.Button("Translate")
            out_audio=gr.Audio()
            out_text=gr.Markdown()

        with gr.Tab("Audio File"):
            audio_file=gr.Audio(type="filepath")
            target2=gr.Dropdown(list(LANGUAGE_CODES.keys()),value="French")
            btn2=gr.Button("Translate Audio")
            out_audio2=gr.Audio()
            out_text2=gr.Markdown()

        with gr.Tab("Record Audio"):
            recorded=gr.Audio(type="filepath",sources=["microphone"])
            target3=gr.Dropdown(list(LANGUAGE_CODES.keys()),value="French")
            btn3=gr.Button("Translate Recorded")
            out_audio3=gr.Audio()
            out_text3=gr.Markdown()

        with gr.Tab("Live Chat Practice"):
            practice=gr.Dropdown(["English","Hindi","Tamil","Telugu","French","Spanish"])
            chat=gr.Chatbot()
            inp=gr.Textbox()
            send=gr.Button("Send")
            state=gr.State([])
            send.click(language_teacher,[inp,practice,state],[chat,inp])

        with gr.Tab("Custom Vocabulary"):
            w=gr.Textbox(label="Word")
            m=gr.Textbox(label="Meaning")
            e=gr.Textbox(label="Example")
            t=gr.Textbox(label="Translation")
            add=gr.Button("Add")
            display=gr.Markdown()

            add.click(lambda a,b,c,d:(add_vocab(a,b,c,d),show_vocab()),
                      [w,m,e,t],[display,display])

            demo.load(show_vocab,None,display)

        with gr.Tab("Words to Gestures"):
            word_input=gr.Textbox(label="Enter Words")
            gesture_lang_dropdown=gr.Dropdown(
                list(LANGUAGE_GESTURE_CONFIG.keys()),
                value="American",
                label="Language"
            )
            gesture_output=gr.Gallery(columns=6,height=200)
            word_btn=gr.Button("Convert")
            word_btn.click(words_to_gestures,
                           [word_input,gesture_lang_dropdown],
                           [gesture_output])

    btn.click(process_input,
              [text_input,gr.State(None),gr.State(None),input_lang,target_lang],
              [out_audio,out_text])

    btn2.click(process_input,
               [gr.State(None),audio_file,gr.State(None),input_lang,target2],
               [out_audio2,out_text2])

    btn3.click(process_input,
               [gr.State(None),gr.State(None),recorded,input_lang,target3],
               [out_audio3,out_text3])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1",server_port=7861,share=False)
