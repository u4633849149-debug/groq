import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Groq API Key aus den Umgebungsvariablen
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY wurde nicht gefunden!")

client = Groq(api_key=api_key)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Roblox NPC API läuft!"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        # JSON vom Roblox-Spiel empfangen
        data = request.get_json(silent=True) or {}

        print("📥 Empfangene Daten:", data)

        # Nachricht des Spielers holen
        user_message = data.get("message")

        if not user_message:
            print("❌ Keine Nachricht erhalten!")

            return jsonify({
                "reply": "Ich habe deine Nachricht nicht bekommen!"
            }), 400

        print("👤 Spieler schreibt:", user_message)

        # Nachricht an Groq senden
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ein cooler NPC in einem Roblox-Spiel. "
                        "Antworte direkt auf das, was der Spieler schreibt. "
                        "Gehe immer auf seine konkrete Nachricht ein. "
                        "Antworte immer auf Deutsch. "
                        "Sei abwechslungsreich, natürlich und freundlich. "
                        "Wiederhole nicht ständig dieselben Antworten. "
                        "Antworte maximal in 1-2 Sätzen."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=60,
            temperature=0.8
        )

        # Antwort der KI
        bot_reply = chat_completion.choices[0].message.content.strip()

        print("🤖 NPC antwortet:", bot_reply)

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:
        print("❌ Fehler bei der Groq-Anfrage:", e)

        return jsonify({
            "reply": "Ups, da ist etwas schiefgelaufen!"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
