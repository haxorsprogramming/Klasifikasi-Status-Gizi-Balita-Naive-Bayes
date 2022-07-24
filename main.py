from flask import Flask, redirect, url_for, render_template, request, jsonify 
import pandas as pd

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:6000/"

@app.route('/')
def index():
    dr = {'BASE_URL' : BASE_URL}
    return render_template('home.html', dRes=dr)

@app.route('/data-balita')
def data_balita():
    dataBalita = pd.read_excel("data/DATA_DUMMY.xlsx", index_col=0)
    dbnp = dataBalita.to_numpy()
    
    return render_template('data-balita.html')

# if __name__ == '__main__':
app.run(host='0.0.0.0', port=7001)