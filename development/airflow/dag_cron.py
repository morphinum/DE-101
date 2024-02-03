from datetime import datetime, timedelta

from airflow import DAG 
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'sigiswald',
    'retries': 5,   
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_cron_v03',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 14 * * 1-2',
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo Hi'
    )
    task1
