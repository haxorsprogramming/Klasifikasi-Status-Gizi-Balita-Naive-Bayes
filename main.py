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
    dBalita = []
    dataBalita = pd.read_excel("data/DATA_DUMMY.xlsx")
    dbnp = dataBalita.to_numpy()
    ord = 0
    for x in dbnp:
        # print(x[6])
        dSatuan = {}
        dSatuan['ord'] = ord
        dSatuan['nama'] = x[0]
        dSatuan['jk'] = x[1]
        dSatuan['usia'] = x[2]
        dSatuan['berat_badan'] = x[3]
        dSatuan['tinggi_badan'] = x[4]
        dSatuan['lila'] = x[5]
        dSatuan['kelas_gizi'] = x[6]
        dBalita.append(dSatuan)
        ord += 1
        print(x[1])
    # print(dBalita)
    return render_template('data-balita.html', dBalita=dBalita)

@app.route('/data-latih')
def data_latih():
    dBalita = []
    dataBalita = pd.read_excel("data/DATA_DUMMY.xlsx")
    dataBalita.replace({'Jenis_Kelamin':{'JK1':1, 'JK2':2}},inplace=True)
    dataBalita.replace({'Usia':{'U1':1}},inplace=True)
    print(dataBalita)
    return render_template('data-latih.html')

# if __name__ == '__main__':
app.run(host='0.0.0.0', port=7001)