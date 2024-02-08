from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'sigiswald',
    'retries': 5,
    'retry_daily': timedelta(minutes=2)
}

def get_data():
    import requests
    import json

    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data


with DAG(
    dag_id='parsing_data',
    default_args=default_args,
    start_date=datetime(2024, 2, 5),
    description='parsing data from https://randomuser.me/',
    schedule='@daily',
    catchup=False) as dag:
    
    streaming_data_task = PythonOperator(
        task_id='get_data',
        python_callable=get_data
    )

    formating_data_task = PythonOperator(
        task_id='format_data',
        python_callable=format_data
    )

    formating_data_task << streaming_data_task