from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import ask_question, update_pdf_text, reset_pdf_context
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded_pdfs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"response": "❌ Please ask a valid question."}), 400

        response = ask_question(message)
        if response is None or response == "":
            response = "🤖 Neo couldn't find an answer. Try rephrasing your question."

        return jsonify({"response": str(response)})

    except Exception as e:
        return jsonify({"response": f"⚠️ Internal Error: {str(e)}"}), 500


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({"message": "❌ No file part in the request"}), 400

        file = request.files['pdf']

        if file.filename == "":
            return jsonify({"message": "❌ No selected file"}), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"message": "❌ Invalid file type. Please upload a PDF."}), 400

        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        update_pdf_text(save_path)

        return jsonify({"message": "✅ PDF uploaded and processed successfully!"})

    except Exception as e:
        return jsonify({"message": f"⚠️ Failed to process PDF: {str(e)}"}), 500


@app.route("/reset_pdf", methods=["POST"])
def reset_pdf():
    try:
        reset_pdf_context()
        return jsonify({"message": "✅ PDF context cleared!"})
    except Exception as e:
        return jsonify({"message": f"⚠️ Failed to reset context: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
