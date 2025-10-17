import os, pickle
from flask import Flask, render_template, request

BASE = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(BASE, "templates"))

MODEL_PATH = os.path.join(BASE, "model.pkl")
VECT_PATH = os.path.join(BASE, "vectorizer.pkl")

print("BASE dir:", BASE)
print("TEMPLATES contents:", os.listdir(os.path.join(BASE,"templates")) if os.path.isdir(os.path.join(BASE,"templates")) else "No templates dir")

try:
    with open(MODEL_PATH,"rb") as f:
        model = pickle.load(f)
    with open(VECT_PATH,"rb") as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print("Warning: model files missing or not loaded:", e)
    model = None
    vectorizer = None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    review = request.form.get("review","").strip()
    if not review:
        return render_template("result.html", error="Please enter review text.")
    if model is None or vectorizer is None:
        return render_template("result.html", error="Model files missing. Run training first.")
    X = vectorizer.transform([review])
    pred = model.predict(X)[0]
    try:
        proba = model.predict_proba(X).max()
    except Exception:
        proba = None
    label = "truthful" if pred == 1 else "deceptive"
    proba_pct = f"{proba*100:.2f}%" if proba is not None else "N/A"
    return render_template("result.html", review=review, label=label, probability=proba_pct)

if __name__ == "__main__":
    app.run(debug=True)


