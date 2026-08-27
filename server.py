import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY wurde nicht gefunden!")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = (
    "Du bist ein freundlicher NPC in einem Roblox-Spiel. "
    "Antworte immer kurz, direkt und auf Deutsch in maximal 1 bis 2 Sätzen. "
    "Schreibe keinen erklärenden Text, sondern direkt die gesprochene Antwort."
)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "Hallo")

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=50,
            temperature=0.7
        )

        # Sicherer Zugriff auf den Antwort-Text
        bot_reply = ""
        if chat_completion.choices and len(chat_completion.choices) > 0:
            message_obj = chat_completion.choices[0].message
            if message_obj and message_obj.content:
                bot_reply = message_obj.content.strip()

        if not bot_reply:
            bot_reply = "Hey du!"

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Fehler bei der Groq-Anfrage: {e}")
        return jsonify({"reply": "Hmm..."}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "Roblox NPC API läuft!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
