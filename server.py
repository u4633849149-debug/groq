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
    "Du antwortest kurz, cool und auf Deutsch. "
    "Maximal 1-2 Sätze, damit es wie ein echter Chat im Spiel wirkt."
)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "Hallo")

        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Das aktuelle, funktionierende Standardmodell
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=60,
            temperature=0.7
        )

        bot_reply = chat_completion.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Fehler bei der Groq-Anfrage: {e}")
        return jsonify({"reply": "Hmm, ich habe gerade Verbindungsprobleme..."}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "Roblox NPC API läuft!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
