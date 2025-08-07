from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os
import requests
import zipfile

app = Flask(__name__)

MODEL_PATH = "model"
MODEL_URL = "https://www.dropbox.com/scl/fi/0tyljfftdi46rlfwsb1ia/gpt2-finetuned.zip?rlkey=zx5nwk943nwp7i9pxsmo8b5s3&st=7bg7d0nn&dl=1"  # Replace with your direct download link

def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH, exist_ok=True)
        zip_path = os.path.join(MODEL_PATH, "model.zip")
        print("Downloading model from Dropbox...")
        r = requests.get(MODEL_URL)
        with open(zip_path, "wb") as f:
            f.write(r.content)
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(MODEL_PATH)
        os.remove(zip_path)
        print("Model ready.")

download_model()
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.eval()

@app.route("/", methods=["GET"])
def home():
    return "GPT-2 Web Server Running."

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "Once upon a time")
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"result": generated_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
