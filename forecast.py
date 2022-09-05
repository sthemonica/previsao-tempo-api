import requests
import pandas as pd
import numpy as np
import json
import pymongo


# user = db_user
# Senha = 7G5UvvXg#RMX$CF
client = pymongo.MongoClient('mongodb+srv://db_user:7G5UvvXg#RMX$CF@api-weather.pe5dlms.mongodb.net/?retryWrites=true&w=majority')
db = client.get_database('api_ow')
collection = db.get_collection('ow_sthe')


api_token = '0ee362fe2f41b058bb688771a9a23142'
city = 'curitiba'
hours = '96'

forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={hours}&appid={api_token}&units=metric&lang=pt_br'
req = requests.get(forecast)
req_dic= req.json()

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

previsao = df1.to_json(orient="index")
prev_json = json.loads(previsao)
json.dumps(prev_json, indent=2) 

collection.insert_many([prev_json])