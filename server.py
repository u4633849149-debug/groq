import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Holt den Key sicher aus den Render-Einstellungen (Environment Variables)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "Du bist ein freundlicher NPC in einem Roblox-Spiel. "
    "Du antwortest kurz, cool und auf Deutsch (maximal 1-2 Sätze), "
    "damit es wie ein echter Chat im Spiel wirkt."
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "Hallo")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.1-8b-instant",  # Aktualisiertes, stabiles Modell
            max_tokens=60,
        )
        bot_reply = chat_completion.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        # Gibt den genauen Fehler zur Diagnose in den Render-Log aus
        print(f"Fehler bei der Groq-Anfrage: {e}")
        return jsonify({"reply": "Hmm, ich habe gerade Verbindungsprobleme..."}), 500

if __name__ == "__main__":
    # Render weist automatisch einen Port zu
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
