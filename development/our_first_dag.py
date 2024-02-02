from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'sigiswald',
    'retries': 2,
    'retre_daily': timedelta(minutes=2)
}

with DAG(
    dag_id='our_first_dag_v4',
    default_args=default_args,
    description='This the first dag I have written',
    start_date=datetime(2024, 2, 1, 2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo Hello, World!'
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo second command'
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo third command at the time of second one!'
    )

    task1 >> [task2, task3]