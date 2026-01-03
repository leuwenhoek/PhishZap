from flask import Flask
import pickle
import os
import re

absolute_path_file = os.path.abspath("Model")
vector = pickle.load(open(os.path.join('Model',"vectorize.pkl"),'rb'))
model = pickle.load(open(os.path.join('Model',"model.pkl"),'rb'))

url = "github.com"

cleaned_url = re.sub(r'^https?://(www\.)?','',url)
predict = model.predict(vector.transform([cleaned_url]))[0]

app