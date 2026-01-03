from flask import Flask, request, render_template,jsonify
import pickle
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT,"PhishZap","Web","templates"), static_folder=os.path.join(PROJECT_ROOT,"PhishZap","Web","static"))

URLchecker_vector = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap", "Model", "URL checker", "vectorize.pkl"), 'rb'))
URLchecker_model = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap",'Model',"URL checker","model.pkl"),'rb'))


MSGchecker_vector = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap", "Model", "MSG checker", "MSGchecker_vectorizer.pkl"), 'rb'))
MSGchecker_model = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap",'Model',"MSG checker","MSGchecker_model.pkl"),'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/URL_check', methods=['GET', 'POST'])
def url_check():
    if request.method == 'POST':
        url = request.form.get('url') 
        cleaned_url = re.sub(r'^https?://(www\.)?','', url)        
        prediction = URLchecker_model.predict(URLchecker_vector.transform([cleaned_url]))[0]
        if prediction == "bad" or prediction == "1" or prediction == 1:
            return jsonify({"status": "scam", "message": "🚨 Malicious URL Detected!"})
        else:
            return jsonify({"status": "safe", "message": "✅ This URL appears to be Healthy."})
    return render_template('URL_check.html')
        

@app.route('/msg_check', methods=['GET', 'POST'])
def MSG_check():
    if request.method == 'POST':
        msg = request.form.get('message') 
        
        if not msg:
            return jsonify({"status": "safe", "message": "No input detected."})

        msg_vector = MSGchecker_vector.transform([msg])  
        prediction = MSGchecker_model.predict(msg_vector) 
        
        if str(prediction[0]).lower() == "bad" or prediction[0] == 1:
            return jsonify({
                "status": "scam", 
                "message": "🚨 THREAT DETECTED: Our AI identified high-risk patterns associated with phishing and social engineering."
            })
        else:
            return jsonify({
                "status": "safe", 
                "message": "✅ MESSAGE SECURE: No malicious intent or fraudulent signatures were detected by the neural engine."
            })
        
    return render_template('msg_check.html')

@app.route("/report",methods=['GET',"POST"])
def report():
    return render_template('report.html')


@app.route('/report_crime', methods=['GET', 'POST'])
def report_crime():
    if request.method == 'POST':
        name = request.form.get('name')
        incident_type = request.form.get('type')
        target = request.form.get('target')
        details = request.form.get('details')
        return jsonify({"status": "success", "message": "Report logged"}), 200

    return render_template('report.html')

@app.route('/library')
def lib():
    return render_template('library.html')

load_dotenv()

API_KEYS = [
    os.getenv("GEMINI_KEY_1"),
    os.getenv("GEMINI_KEY_2"),
    os.getenv("GEMINI_KEY_3"),
    os.getenv("GEMINI_KEY_4"),
    os.getenv("GEMINI_KEY_5")
]

@app.route('/zap_bot', methods=['GET', 'POST'])
def zap_bot():
    if request.method == 'POST':
        user_query = request.form.get('message')
        reply = None

        for key in API_KEYS:
            if not key: continue  
            try:
                client = genai.Client(api_key=key)
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    config=types.GenerateContentConfig(
                        system_instruction="You are Zap Bot, a cyber-security AI for the PhishZap project. Be concise, use technical terms, and help users identify phishing threats.",
                    ),
                    contents=user_query
                )
                
                reply = response.text
                break  
            except Exception as e:
                print(f"Key failed: {key[:8]}... Error: {e}")
                continue  
        if reply is None:
            reply = "CRITICAL ERROR: All Neural Uplinks (API Keys) are exhausted or invalid."

        return jsonify({"reply": reply})

    return render_template('Zap_bot.html')

@app.route("/about")

def about_team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)
