# Aplicação backend Python utilizando API Open Weather

A sigla API siginifica **Application Programming Interface** (Interface de Programação de Aplicação). Por meio de APIs conseguimos criar sofwtares capazes de se comunicar com diversas plataformas de uma forma simples e rápida.

O site [Open Weather Map](https://openweathermap.org/) nos oferece dados do clima em nível mundial como, por exemplo, temperatural atual e previsão para os próximos 4 dias (com timestamps de 3 em 3 horas) que são gratuitos e podem ser utilizados limitadamente somente criando um login na plataforma.

## Parte I
Neste projeto você encontrará uma aplicação em Python utilizando a API do site Open Weather para a coletar a previsão dos próximos dias com o [**Hourly forecast**](https://openweathermap.org/api/hourly-forecast), fazer o tratamento dessas informações e guardá-las tratradas em um banco de dados não relacional, que neste caso é o MongoDB. O notebook responsável por essa etapa é o [`forecast.py`](https://github.com/sthemonica/previsao-tempo-api/blob/main/forecast.py).


## Parte II
A segunda parte é transformar essa aplicação da **Parte I** em uma API e fazer com que todas essas partes sejam integradas com o Flask. Porém, como ainda é uma das ferramentas que estou aprendendo, preciso entender melhor como a integração entre as ferramentas funciona. Para acessar o que foi feito até agora dos meus estudos do Flask e integração de ferramentas você pode acessar o arquivo [`main.py`](https://github.com/sthemonica/previsao-tempo-api/blob/main/main.py).

## Ambiente
