#-------------------Bibliotecas------------------------
from http import client
from typing import Collection
import requests
import pandas as pd
import pymongo
import json
import re


#-----------------Trazendo os dados da API---------------
#
# Como o projeto será para previsão do tempo de 5 dias, será utilizado o máximo de timestamps (pontos definidos de hora)
# possíveis que podem ser utilziados no modo de Hourly forecast, que são 96 timestamps, dessa forma teremos a previsão para uma
# quantidade de 96 horas a frente. Também é necessário retirar a previsão do tempo do dia atual

#---------------------Variáveis--------------------------
#
api_token = "0ee362fe2f41b058bb688771a9a23142"
city = "curitiba"
hours = "96"
days = "5"

#-----------------------------URLS------------------------
#current = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_token}&lang=pt_br"
forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={hours}&appid={api_token}&lang=pt_br"

# Fazendo as requisições diárias
#req_today = requests.get(current)
#req_today_dic = req_today.json()
#req_today_dic
#print(req_today_dic)

#-----------------Obtendo as requests---------------------
# 
req = requests.get(forecast)
req_dic = req.json()
req_dic
#print(req_dic)

#--------------Tratando os dados-----------------------
df = pd.json_normalize(req_dic, record_path=['list'], errors='ignore')
df1 = df.loc[:,'dt_txt':'main.feels_like']
column_names = {'dt_txt':'dia', 'main.temp':'temp', 'main.feels_like':'sensacao'}
df1.rename(columns = column_names, inplace=True)

#Separando as colunas de dia e hora
df1['hora'] = df1['dia']
df1['hora'] = df1['hora'].apply(lambda x: x[11:])
df1['dia'] = df1['dia'].apply(lambda x: x[:-9])
df1=df1[['dia','hora', 'temp', 'sensacao']]

# de Kelvin para Celsius
conversion = 273.15
df1['temp'] = df1['temp'] - conversion
df1['sensacao'] = df1['sensacao'] - conversion


previsao = df1.to_json(orient="index")
prev_json = json.loads(previsao)
json.dumps(prev_json, indent=2) 


#-------------------Conectando o bd--------------------
# user = db_user
# Senha = 7G5UvvXg#RMX$CF

client = pymongo.MongoClient("mongodb+srv://db_user:7G5UvvXg#RMX$CF@api-weather.pe5dlms.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('api_ow')

collection = db.get_collection('ow_sthe')

#-------------------Inserindo os dados no bd---------------------
# 

collection.insert_many([prev_json])

#------------------Trazendo os dados novamente----------------------
#resultado = collection.find({})



