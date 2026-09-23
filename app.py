from flask import Flask, jsonify, render_template, request

from models.classifier import MedicalQueryClassifier
from services.medical_filter import validate_query
from services.medical_llm import MedicalLLM

app = Flask(__name__)
classifier = MedicalQueryClassifier()
medical_llm = MedicalLLM()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"ok": False, "error": "Please enter a question."}), 400

    validation = validate_query(question)
    if not validation["allowed"]:
        return jsonify({
            "ok": True,
            "allowed": False,
            "classification": validation["reason"],
            "answer": validation["message"],
        })

    prediction = classifier.predict(question)
    if not prediction["is_medical"]:
        return jsonify({
            "ok": True,
            "allowed": False,
            "classification": "non-medical",
            "confidence": prediction["confidence"],
            "answer": (
                "This system is designed only for medical and clinical questions. "
                "Please ask a medical or healthcare-related question."
            ),
        })

    answer = medical_llm.answer(question, emergency=validation["emergency"])
    return jsonify({
        "ok": True,
        "allowed": True,
        "classification": prediction["label"],
        "confidence": prediction["confidence"],
        "emergency": validation["emergency"],
        "answer": answer,
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
