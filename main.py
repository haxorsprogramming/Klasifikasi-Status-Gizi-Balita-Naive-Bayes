import imp
from flask import Flask, redirect, url_for, render_template, request, jsonify 
import pandas as pd
import json
import numpy as np
import random
# from csv import reader
from fungsi import predict, str_column_to_float, str_column_to_int, summarize_by_class, load_csv

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
    dataBalita.replace({'Usia':{'U1':1, 'U2':2, 'U3':3, 'U4':4, 'U5':5}},inplace=True)
    dataBalita.replace({'Berat_Badan':{'BB1':1,'BB2':2,'BB3':3,'BB4':4,'BB5':5,'BB6':6,'BB7':7,'BB8':8,'BB9':9,'BB10':10}}, inplace=True)
    dataBalita.replace({'Tinggi_Badan':{'TB1':1,'TB2':2,'TB3':3,'TB4':4,'TB5':5,'TB6':6,'TB7':7,'TB8':8,'TB9':9,'TB10':10}}, inplace=True)
    dataBalita.replace({'Lila':{'LL1':1, 'LL2':2, 'LL3':3, 'LL4':4, 'LL5':5}},inplace=True)
    dataBalita.replace({'Kelas_Gizi':{'Gizi Lebih':4,'Gizi Baik':3, 'Gizi Kurang':2, 'Gizi Buruk':1}},inplace=True)
    dbnp = dataBalita.to_numpy()
    ord = 1
    rpJk = {'JK1':0, 'JK2':0, 'total':0}
    rpUsia = {'U1':0,'U2':0,'U3':0,'U4':0,'U5':0, 'total':0}
    rpBb = {'BB1':0,'BB2':0,'BB3':0,'BB4':0,'BB5':0,'BB6':0,'BB7':0,'BB8':0,'BB9':0,'BB10':0, 'total':0}
    rpTb = {'TB1':0,'TB2':0,'TB3':0,'TB4':0,'TB5':0,'TB6':0,'TB7':0,'TB8':0,'TB9':0,'TB10':0, 'total':0}
    rpLl = {'LL1':0,'LL2':0,'LL3':0,'LL4':0,'LL5':0,'total':0}
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
        # normalisasi berat badan 
        if x[3] == 1:
            rpBb['BB1'] += 1
        elif x[3] == 2:
            rpBb['BB2'] += 1
        elif x[3] == 3:
            rpBb['BB3'] += 1
        elif x[3] == 4:
            rpBb['BB4'] += 1
        elif x[3] == 5:
            rpBb['BB5'] += 1
        elif x[3] == 6:
            rpBb['BB6'] += 1
        elif x[3] == 7:
            rpBb['BB7'] += 1
        elif x[3] == 8:
            rpBb['BB8'] += 1
        elif x[3] == 9:
            rpBb['BB9'] += 1
        else:
            rpBb['BB10'] += 1
        # normalisasi tinggi badan 
        if x[4] == 1:
            rpTb['TB1'] += 1
        elif x[4] == 2:
            rpTb['TB2'] += 1
        elif x[4] == 3:
            rpTb['TB3'] += 1
        elif x[4] == 4:
            rpTb['TB4'] += 1
        elif x[4] == 5:
            rpTb['TB5'] += 1
        elif x[4] == 6:
            rpTb['TB6'] += 1
        elif x[4] == 7:
            rpTb['TB7'] += 1
        elif x[4] == 8:
            rpTb['TB8'] += 1
        elif x[4] == 9:
            rpTb['TB9'] += 1
        else:
            rpTb['TB10'] += 1
        # normalisasi ll
        if x[5] == 1:
            rpLl['LL1'] += 1
        elif x[5] == 2:
            rpLl['LL2'] += 1
        elif x[5] == 3:
            rpLl['LL3'] += 1
        elif x[5] == 4:
            rpLl['LL4'] += 1
        else:
            rpLl['LL5'] += 1
    # total 
    rpJk['total'] = rpJk['JK1'] + rpJk['JK2']
    rpUsia['total'] = rpUsia['U1'] + rpUsia['U2'] + rpUsia['U3'] + rpUsia['U4'] + rpUsia['U5']
    rpBb['total'] = rpBb['BB1'] + rpBb['BB2'] + rpBb['BB3'] + rpBb['BB4'] + rpBb['BB5'] + rpBb['BB6'] + rpBb['BB7'] + rpBb['BB8'] + rpBb['BB9'] + rpBb['BB10']
    rpTb['total'] = rpTb['TB1'] + rpTb['TB2'] + rpTb['TB3'] + rpTb['TB4'] + rpTb['TB5'] + rpTb['TB6'] + rpTb['TB7'] + rpTb['TB8'] + rpTb['TB9'] + rpTb['TB10']
    rpLl['total'] = rpLl['LL1'] + rpLl['LL2'] + rpLl['LL3'] + rpLl['LL4'] + rpLl['LL5']
    return render_template('data-latih.html', dBalita=dBalita, rpJk=rpJk, rpUsia=rpUsia, rpBb=rpBb, rpTb=rpTb, rpLl=rpLl)

@app.route('/data-validasi')
def data_validasi():
    return render_template('data-validasi.html')

# @app.route('/proses-klasifikasi')
@app.route('/proses-klasifikasi')
def proses_klasifikasi():
    return render_template('proses-klasifikasi.html')

@app.route('/hasil-klasifikasi', methods=('GET', 'POST'))
def hasil():
    nama = request.form['txtNamaBalita']
    jk = request.form['txtJenisKelamin']
    bb = request.form['txtBeratBadan']
    tb = request.form['txtTinggiBadan']
    usia = request.form['txtUsia']
    ll = request.form['txtLingkarLengan']

    at = usia[0:2]
    # print(int(ambilTahun))

    cbb = 0
    ctb = 0
    cll = 0
    cu = 0

    if int(at) >= 0:
        cu = 1
    if int(at) >= 1:
        cu = 2
    if int(at) >= 2:
        cu = 3
    if int(at) >= 3:
        cu = 4
    if int(at) >= 4:
        cu = 5

    if int(ll) >= 1 and int(ll) <= 5:
        cll = 1
    if int(ll) >= 6 and int(ll) <= 10:
        cll = 2
    if int(ll) >= 11 and int(ll) <= 15:
        cll = 3
    if int(ll) >= 16 and int(ll) <= 20:
        cll = 4
    if int(ll) >= 21 and int(ll) <= 25:
        cll = 5

    if int(bb) >= 0 and int(bb) <= 3:
        cbb = 1
    if int(bb) >= 4 and int(bb) <= 6:
        cbb = 2
    if int(bb) >= 7 and int(bb) <= 9:
        cbb = 3
    if int(bb) >= 10 and int(bb) <= 12:
        cbb = 4
    if int(bb) >= 13 and int(bb) <= 15:
        cbb = 5
    if int(bb) >= 16 and int(bb) <= 18:
        cbb = 6
    if int(bb) >= 19 and int(bb) <= 21:
        cbb = 7
    if int(bb) >= 22 and int(bb) <= 24:
        cbb = 8
    if int(bb) >= 25 and int(bb) <= 27:
        cbb = 9
    if int(bb) >= 28 and int(bb) <= 30:
        cbb = 10

    if int(tb) > 0 and int(tb) < 20:
        ctb = 1
    if int(tb) > 21 and int(tb) < 30:
        ctb = 2
    if int(tb) > 31 and int(tb) < 40:
        ctb = 3
    if int(tb) > 41 and int(tb) < 50:
        ctb = 4
    if int(tb) > 52 and int(tb) < 60:
        ctb = 5
    if int(tb) > 61 and int(tb) < 70:
        ctb = 6
    if int(tb) > 71 and int(tb) < 80:
        ctb = 7
    if int(tb) > 81 and int(tb) < 90:
        ctb = 8
    if int(tb) > 91 and int(tb) < 100:
        ctb = 9
    if int(tb) > 101 and int(tb) < 110:
        ctb = 10
    

    # Make a prediction with Naive Bayes on Iris Dataset
    filename = 'data/training.csv'
    dataset = load_csv(filename)
    for i in range(len(dataset[0])-1):
        str_column_to_float(dataset, i)
    # convert class column to integers
    dClass = str_column_to_int(dataset, len(dataset[0])-1)
    str_column_to_int(dataset, len(dataset[0])-1)
    # fit model
    model = summarize_by_class(dataset)
    # define a new record
    row = [int(jk),int(cu),int(cbb),int(ctb),int(cll)]
    # predict the label
    label = predict(model, row)
    # return label
    # print('Data=%s, Predicted: %s' % (row, label))

    # predict()

    hasil = ""
    if dClass['GiziBaik'] == label:
        hasil = "Gizi Baik"
    if dClass['GiziBuruk'] == label:
        hasil = "Gizi Buruk"
    if dClass['GiziKurang'] == label:
        hasil = "Gizi Kurang"
    if dClass['GiziLebih'] == label:
        hasil = "Gizi Lebih"
    # print(dClass['GiziBaik'])
    
    data = {'status':label, 'class' : dClass, 'hasil':hasil}
    # return jsonify(data)
    return render_template('hasil-klasifikasi.html', dr=data)

# if __name__ == '__main__':
app.run(host='0.0.0.0', port=7001)