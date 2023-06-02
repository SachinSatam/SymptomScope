from flask import Flask, render_template, url_for, flash, redirect,send_file
import joblib
from flask import request
import matplotlib
from matplotlib.style import use
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
matplotlib.use('Agg')
import random
import os
app = Flask(__name__, template_folder='templates')

@app.route("/")

@app.route("/Diabetes")
def cancer():
    return render_template("diabetes.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==6):
        loaded_model = joblib.load(r'C:\Users\91810\Desktop\Project\Health-App-main\Health-App-main\Diabetes_API\diabetes_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    if request.method == "POST":
        Pregnancies=int(request.form['Pregnancies'])
        Glucos=int(request.form['Present_Price'])
        BloodPressure=int(request.form['BloodPressure'])
        BMI=int(request.form['BMI'])
        DiabetesPedigreeFunction=int(request.form['DiabetesPedigreeFunction'])
        Age=int(request.form['Age'])
        labels=['Pregnancies','Glucose','BloodPressure','BMI','Age']
        inputs=[Pregnancies,Glucos,BloodPressure,BMI,Age]
        avg_val=[3,120,69,31,33]
        plt.rcParams['figure.figsize']=(10,10)
        plt.plot(labels,inputs,label='User values')
        plt.plot(labels,avg_val,label='Avg values')
        plt.xlabel('inputs')
        plt.ylabel('values')
        plt.legend()
        plt.title('comparison')
        x=range(100)
        num=random.choice(x)
        plt.savefig('static/plot{}.png'.format(num))
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
         #diabetes
        if(len(to_predict_list)==6):
            result = ValuePredictor(to_predict_list,6)
    
    if(int(result)==1):
        prediction = "Disease may get severe"
    else:
        prediction = "Disease may not get severe"
    return(render_template("result.html", prediction_text=prediction,plot_url='static/plot{}.png'.format(num)))    

if __name__ == "__main__":
    app.run(debug=True)
