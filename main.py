import requests
import pandas as pd
import numpy as np
from flask import Flask
from flask_mongoengine import MongoEngine

#
api_token = '0ee362fe2f41b058bb688771a9a23142'
city = 'curitiba'
hours = '96'
#---
forecast = 'http://api.openweathermap.org/data/2.5/forecast?q='+city+'&cnt='+hours+'&appid='+api_token+'&units=metric&lang=pt_br'
req = requests.get(forecast)
req_dic= req.json()
#

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'api_ow',
    'host':'localhost',
    'port':'27017'
}

app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/api_ow'
}

db = MongoEngine(app)
db.init_app(app)

class forecast(db.Document):
    dia = db.FloatField()
    temp = db.FloatField()
    sensacao = db.FloatField()
    umidade = db.IntField()
    cidade = db.StringField(required=True)

@app.route('/owforecast', methods=['GET', 'POST'])

def dados_dias(api_token, city, hours):
    forecast = 'http://api.openweathermap.org/data/2.5/forecast?q='+city+'&cnt='+hours+'&appid='+api_token+'&units=metric&lang=pt_br'
    req = requests.get(forecast)
    req_dic= req.json()

    #--------------Tratando os dados-----------------------
    df = pd.json_normalize(req_dic)
    df_n = pd.json_normalize(req_dic, record_path=['list'], errors='ignore')
    df1 = df_n.loc[:,'dt_txt':'main.humidity']
    df1 = df1.drop(['main.temp_min',	'main.temp_max','main.pressure', 'main.sea_level', 'main.grnd_level'], axis=1)
    df1['cidade'] = df['city.name']
    column_names = {'dt_txt':'dia', 'main.temp':'temp', 'main.feels_like':'sensacao', 'main.humidity':'umidade', 'cidade':'cidade'}
    df1.rename(columns = column_names, inplace=True)
    df1 = df1.replace(np.nan,'Curitiba')
    df1['hora'] = df1['dia']
    df1['hora'] = df1['hora'].apply(lambda x: x[11:])
    df1['dia'] = df1['dia'].apply(lambda x: x[:-9])
    df1=df1[['cidade','dia','hora', 'temp', 'sensacao', 'umidade']]
    result = Flask.jsonify(df1)   
    
    Flask('Calculando previsão do tempo', 'success')
    return (Flask.jsonify(df1))

    
@app.route('/', methods=['POST'])
def index_post():
    def add_many():
        db = client.get_database('api_ow')
        collection = db.get_collection('ow_sthe')
        collection.insert_many([result])
    return Flask.jsonify(message="success")