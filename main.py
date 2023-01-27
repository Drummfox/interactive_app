import streamlit as st
import pandas as pd
import requests
from datetime import datetime

header = st.container()
dataset = st.container()
settings = st.sidebar.container()
model_training = st.container()

def get_data(api):
    '''
    Получает данные по api
    '''

    data = requests.get(api)
    return data.json()['data']



def get_asset(dictionary_):
    '''
    Формирует словарь с доступными списками валют и их id
    '''
    dict2 = {}
    for item in dictionary_:
        dict2[item['symbol']] = 'https://api.coincap.io/v2/assets/'+ item['id'] + '/history?interval=d1' 
    return dict2

def get_asset_list(dictionary_):
    '''
    Формирует список с доступными списками валют и их id
    '''
    list_assets = []
    for item in dictionary_:
        list_assets.append(item['symbol'])
    return list_assets

def date (history):
    '''
    Формирует список дат 
    '''    
    data_list = []
    for item in history:
        date = (item['date']).split('T')[0]
        date1 = datetime.strptime(date, '%Y-%m-%d')
        date2 = date1.date()
        data_list.append(date2)
    return data_list

def value (history):
    '''
    Формирует список цены 
    '''
    data_list = []
    for item in history:
        data_list.append(float(item['priceUsd']))
    return data_list
   
    
with settings:
    sel_col, disp_col = st.columns(2)
    dict_ = get_data('https://api.coincap.io/v2/assets')
    asset_list = get_asset_list(dict_)
    asset = sel_col.selectbox('Select an asset', options=asset_list)
    api = get_asset(dict_)
    history = get_data(api[asset])
    date_ = date(history)
    value_ = value(history)
    date_from = st.date_input('Date from', value = min(date_), min_value = min(date_), max_value = max(date_))
    date_to = st.date_input('Date to', value = max(date_), min_value = min(date_), max_value = max(date_))

    

with header:
    st.title('Exchange rate')

with dataset:
    start_index = date_.index(date_from)
    end_index = date_.index(date_to)
   
    exchange_rate = pd.DataFrame({
    'date': date_[start_index : end_index],
    'rate': value_[start_index : end_index]
    })
    
    # st.write(exchange_rate)


    st.bar_chart(exchange_rate, x = 'date', y = 'rate')
