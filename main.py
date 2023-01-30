import streamlit as st
import pandas as pd
import requests
from datetime import datetime

header = st.container()
dataset_ = st.container()
settings = st.sidebar.container()

def dataset(api) -> list:
    '''
    Получает данные по api
    '''

    data = requests.get(api)
    return data.json()['data']



def get_asset(dictionary) -> dict:
    '''
    Формирует словарь с доступными списками валют и их id
    '''
    symbol_api = {}
    for item in dictionary:
        symbol_api[item['symbol']] = 'https://api.coincap.io/v2/assets/'+ item['id'] + '/history?interval=d1' 
    return symbol_api


def get_date (history) -> list:
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

def get_value (history) -> list:
    '''
    Формирует список цены 
    '''
    data_list = []
    for item in history:
        data_list.append(float(item['priceUsd']))
    return data_list
   
def app():    
    with settings:       
        data = dataset('https://api.coincap.io/v2/assets')
        symbol_list = [item['symbol'] for item in data] 
        
        symbol = st.selectbox('Select an asset', options=symbol_list)
        
        symbol_api = get_asset(data)
        history = dataset(symbol_api[symbol])
        date = get_date(history)
        rate = get_value(history)
       
        date_from = st.date_input('Date from', value = min(date), min_value = min(date), max_value = max(date))
        date_to = st.date_input('Date to', value = max(date), min_value = min(date), max_value = max(date))
        
        start_index = date.index(date_from)
        end_index = date.index(date_to)

        
    with header:
        st.title('Exchange rate')


    with dataset_:   
        exchange_rate = pd.DataFrame({
        'date': date [start_index : end_index],
        'rate': rate [start_index : end_index]
        })
        
        st.bar_chart(exchange_rate, x = 'date', y = 'rate')

if __name__ == '__main__':
    app()