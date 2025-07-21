# --- IMPORTS ---
import gradio as gr
import ollama
import pyttsx3  # For offline Text-to-Speech

# --- TTS SETUP ---
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- OLLAMA SETUP ---
ollama_client = ollama.Client()
DEFAULT_MODEL = "mistral"

# --- COACH FUNCTION ---
def get_genz_advice(user_query, model, mood):
    mood_instruction = {
        "Motivational 💪": "Be uplifting and inspiring, like a hype coach.",
        "Chill 😌": "Be relaxed and comforting, like a best friend giving advice.",
        "Funny 🤪": "Add light humor and Gen Z memes/slang.",
        "Tough Love 🥴": "Be blunt but caring. Like, get real."
    }

    try:
        response = ollama_client.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a Gen Z life coach. {mood_instruction[mood]} Keep answers short, helpful, and use emojis or Gen Z tone."
                },
                {"role": "user", "content": user_query}
            ],
            options={
                "temperature": 0.7,
                "num_predict": 150
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- GRADIO UI ---
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## 💬 Gen Z Life Coach – Talk to Me, Bestie!")
    gr.Markdown("Feeling lost, stressed, or need a vibe check? I'm here for real talk. 💖🌈")

    with gr.Row():
        input_box = gr.Textbox(
            label="🗣️ What’s on your mind?",
            placeholder="e.g., I'm feeling burnt out from college...",
            lines=2
        )
        model_selector = gr.Dropdown(
            ["mistral", "tinyllama", "gemma:2b"],
            label="🧠 Choose Coach Brain",
            value=DEFAULT_MODEL
        )
        mood_selector = gr.Dropdown(
            ["Motivational 💪", "Chill 😌", "Funny 🤪", "Tough Love 🥴"],
            label="💡 Pick a Mood",
            value="Chill 😌"
        )

    submit_btn = gr.Button("Send 📨")
    output_box = gr.Textbox(label="✨ Coach Says...", lines=5)

    # 🔊 Read it Aloud Button
    read_btn = gr.Button("🔊 Read it Aloud")

    def handle_submit(user_input, selected_model, selected_mood):
        response = get_genz_advice(user_input, selected_model, selected_mood)
        speak(response)  # Speak immediately after getting the reply
        return response

    submit_btn.click(
        fn=handle_submit,
        inputs=[input_box, model_selector, mood_selector],
        outputs=output_box
    )

    read_btn.click(
        fn=speak,
        inputs=output_box,
        outputs=[]
    )

# --- LAUNCH ---
demo.launch()