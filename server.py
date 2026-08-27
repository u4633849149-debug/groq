import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# ==========================================
# GROQ API
# ==========================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY wurde nicht gefunden!")

client = Groq(api_key=api_key)


# ==========================================
# STARTSEITE
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Roblox NPC API läuft!"
    })


# ==========================================
# CHAT
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():
    try:

        # ------------------------------------------
        # JSON von Roblox empfangen
        # ------------------------------------------

        data = request.get_json(silent=True) or {}

        print("========================================")
        print("📥 NEUE ANFRAGE")
        print("📦 Empfangene Daten:", data)

        user_message = data.get("message")

        if not user_message:
            print("❌ Keine Nachricht erhalten!")

            return jsonify({
                "reply": "Ich habe deine Nachricht nicht bekommen!"
            }), 400

        user_message = str(user_message).strip()

        print("👤 Spieler schreibt:", repr(user_message))


        # ------------------------------------------
        # Nachricht an Groq senden
        # ------------------------------------------

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ein cooler NPC namens Rig in einem Roblox-Spiel. "

                        "Reagiere IMMER direkt auf das, was der Spieler gerade schreibt. "

                        "Wenn der Spieler dich begrüßt, begrüße ihn zurück. "
                        "Wenn der Spieler eine Frage stellt, beantworte genau diese Frage. "
                        "Wenn der Spieler fragt, wie es dir geht, antworte darauf. "

                        "Antworte immer auf Deutsch. "
                        "Sei locker, freundlich, natürlich und abwechslungsreich. "
                        "Vermeide immer wieder dieselben Antworten. "

                        "Antworte maximal mit 1 bis 2 kurzen Sätzen."
                    )
                },

                {
                    "role": "user",
                    "content": user_message
                }
            ],

            max_tokens=100,
            temperature=0.8
        )


        # ------------------------------------------
        # Groq Antwort überprüfen
        # ------------------------------------------

        print("📦 Groq-Antwort erhalten")

        print("Choices:", len(chat_completion.choices))


        if not chat_completion.choices:

            print("❌ Groq hat keine Choices zurückgegeben!")

            return jsonify({
                "reply": "Hmm... ich habe gerade keine Antwort."
            })


        choice = chat_completion.choices[0]

        print("📦 Choice:", choice)


        # ------------------------------------------
        # Message überprüfen
        # ------------------------------------------

        if not choice.message:

            print("❌ Groq hat keine Message zurückgegeben!")

            return jsonify({
                "reply": "Hmm... ich kann gerade nicht antworten."
            })


        print("📦 Message:", choice.message)


        # ------------------------------------------
        # Content auslesen
        # ------------------------------------------

        bot_reply = choice.message.content


        print("📄 Rohantwort:", repr(bot_reply))


        if bot_reply is None:

            print("❌ Groq Content ist None!")

            bot_reply = ""


        bot_reply = str(bot_reply).strip()


        # ------------------------------------------
        # Leere Antwort verhindern
        # ------------------------------------------

        if not bot_reply:

            print("⚠️ GROQ HAT EINE LEERE ANTWORT GELIEFERT!")

            bot_reply = (
                "Hmm, da bin ich gerade etwas sprachlos. "
                "Frag mich nochmal!"
            )


        print("🤖 NPC antwortet:", repr(bot_reply))
        print("========================================")


        # ------------------------------------------
        # Antwort an Roblox
        # ------------------------------------------

        return jsonify({
            "reply": bot_reply
        })


    except Exception as e:

        print("========================================")
        print("❌ FEHLER BEI DER GROQ-ANFRAGE")
        print("❌ Fehler:", repr(e))
        print("========================================")

        return jsonify({
            "reply": "Ups, bei mir ist gerade etwas schiefgelaufen!"
        }), 500


# ==========================================
# SERVER START
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    print("========================================")
    print("🚀 Roblox NPC API wird gestartet...")
    print("🌐 Port:", port)
    print("🤖 Groq Model: openai/gpt-oss-120b")
    print("========================================")

    app.run(
        host="0.0.0.0",
        port=port
    )
