from flask import Flask, request, render_template
import pickle
import os
import re

app = Flask(__name__)

vector = pickle.load(open(os.path.join('Model',"vectorize.pkl"),'rb'))
model = pickle.load(open(os.path.join('Model',"model.pkl"),'rb'))

@app.route('/URL_check', methods=['GET', 'POST'])
def URL_check():
    if request.method == 'POST':
        url = request.form.get('url') 
        cleaned_url = re.sub(r'^https?://(www\.)?','', url)        
        prediction = model.predict(vector.transform([cleaned_url]))[0]
        print(f"URL: {url} | Prediction: {prediction}")
        if str(prediction).lower() == "bad" or prediction == 1:
            return "Bad URL"
        else:
            return "Healthy URL"
    
    return render_template('url_check.html')
if __name__ == "__main__":
    app.run(debug=True)