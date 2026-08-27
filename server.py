import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY fehlt!")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "Du bist ein freundlicher NPC in einem Roblox-Spiel. "
    "Du antwortest kurz, cool und auf Deutsch. "
    "Maximal 1-2 Sätze, damit es wie ein echter Chat im Spiel wirkt."
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Groq Roblox NPC API läuft!"
    })


@app.route("/models", methods=["GET"])
def models():
    try:
        model_list = client.models.list()

        models = [
            model.id
            for model in model_list.data
        ]

        print("Verfügbare Groq-Modelle:")
        for model in models:
            print(model)

        return jsonify({
            "models": models
        })

    except Exception as e:
        print(f"Fehler beim Abrufen der Modelle: {e}")

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        user_message = data.get("message", "Hallo")

        if not user_message:
            user_message = "Hallo"

        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=60,
            temperature=0.7
        )

        bot_reply = chat_completion.choices[0].message.content

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:
        print(f"Fehler bei der Groq-Anfrage: {e}")

        return jsonify({
            "reply": "Hmm, ich habe gerade Verbindungsprobleme..."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
