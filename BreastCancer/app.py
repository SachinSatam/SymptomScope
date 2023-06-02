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
imgfolder=os.path.join('static','Cancerimg')
app.config['UPLOAD_FOLDER']=imgfolder
@app.route("/")

@app.route("/cancer")
def cancer():
    logo=os.path.join(app.config['UPLOAD_FOLDER'],'logo.png')
    return render_template("cancer.html",logoimg=logo)


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==5):
        loaded_model = joblib.load(r"C:\Users\91810\Desktop\Project\Health-App-main\Health-App-main\BreastCancer\cancer_model.pkl")
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    
    
    if request.method == "POST":
        Concave_points_mean=int(request.form['concave points_mean'])
        area_mean=int(request.form['area_mean'])
        radius_mean=int(request.form['radius_mean'])
        perimeter_mean=int(request.form['perimeter_mean'])
        concavity_mean=int(request.form['concavity_mean'])
        labels=['Concave_points_mean','area_mean','radius_mean','perimeter_mean','concavity_mean']
        inputs=[Concave_points_mean,area_mean,radius_mean,perimeter_mean,concavity_mean]
        avg_val=[0.04,654.88,14.12,91.96,0.08]
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
         #cancer
        if(len(to_predict_list)==5):
            result = ValuePredictor(to_predict_list,5)
    
    if(int(result)==1):
        prediction = "Disease may get severe"
    else:
        prediction = "Disease may not get severe"
    return(render_template("result.html",prediction_text=prediction,plot_url='static/plot{}.png'.format(num)))


if __name__ == "__main__":
   app.run(debug=True)
