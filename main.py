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
    ord = 1
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
        # print(x[1])
    # print(dBalita)
    return render_template('data-balita.html', dBalita=dBalita)

@app.route('/data-latih')
def data_latih():
    dBalita = []
    dataBalita = pd.read_excel("data/DATA_DUMMY.xlsx")
    dataBalita.replace({'Jenis_Kelamin':{'JK1':1, 'JK2':2}},inplace=True)
    dataBalita.replace({'Usia':{'U1':1, 'U1':2, 'U3':3, 'U4':4, 'U5':5}},inplace=True)
    dataBalita.replace({'Berat_Badan':{'BB1':1,'BB2':2,'BB3':3,'BB4':4,'BB5':5,'BB6':6,'BB7':7,'BB8':8,'BB9':9,'BB10':10}},inplace=True)
    dataBalita.replace({'Tinggi_Badan':{'TB1':1,'TB2':2,'TB3':3,'TB4':4,'TB5':5,'TB6':6,'TB7':7,'TB8':8,'TB9':9,'TB10':10}},inplace=True)
    dataBalita.replace({'LiLA':{'LL1':1, 'LL2':2, 'LL3':3, 'LL4':4, 'LL5':5}},inplace=True)
    dataBalita.replace({'Kelas_Gizi':{'Gizi Lebih':4,'Gizi Baik':3, 'Gizi Kurang':2, 'Gizi Buruk':1}},inplace=True)
    dbnp = dataBalita.to_numpy()
    ord = 0
    rpJk = {'JK1':0, 'JK2':0}
    rpUsia = {'U1':0,'U2':0,'U3':0,'U4':0,'U5':0}
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
        # normalisasi jenis kelamin
        if x[1] == 1:
            rpJk['JK1'] += 1
        else:
            rpJk['JK2'] += 1
        # normalisasi usia 
        if x[2] == 1:
            rpUsia['U1'] += 1
        elif x[2] == 2:
            rpUsia['U2'] += 1
        elif x[2] == 3:
            rpUsia['U3'] += 1
        elif x[2] == 4:
            rpUsia['U4'] += 1
        else:
            rpUsia['U5'] += 1

    return render_template('data-latih.html', dBalita=dBalita, rpJk=rpJk, rpUsia=rpUsia)

@app.route('/proses-klasifikasi')
def proses_klasifikasi():

    return render_template('proses-klasifikasi.html')

@app.route('/hasil-klasifikasi')
def hasil():

    return render_template('hasil-klasifikasi.html')

# if __name__ == '__main__':
app.run(host='0.0.0.0', port=7001)