from flask import Flask, request, render_template,jsonify
import pickle
import os
import re

app = Flask(__name__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

URLchecker_vector = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap", "Model", "URL checker", "vectorize.pkl"), 'rb'))
URLchecker_model = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap",'Model',"URL checker","model.pkl"),'rb'))


MSGchecker_vector = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap", "Model", "MSG checker", "MSGchecker_vectorizer.pkl"), 'rb'))
MSGchecker_model = pickle.load(open(os.path.join(PROJECT_ROOT,"PhishZap",'Model',"MSG checker","MSGchecker_model.pkl"),'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/URL_check', methods=['GET', 'POST'])
def URL_check():
    if request.method == 'POST':
        url = request.form.get('url') 
        cleaned_url = re.sub(r'^https?://(www\.)?','', url)        
        prediction = URLchecker_model.predict(URLchecker_vector.transform([cleaned_url]))[0]
        if str(prediction).lower() == "bad" or prediction == 1:
            return "Bad URL"
        else:
            return "Healthy URL"
        

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

if __name__ == "__main__":
    app.run(debug=True)
