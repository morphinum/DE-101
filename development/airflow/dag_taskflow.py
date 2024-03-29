from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner': 'sigiswald',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
        dag_id='dag_taskflow_v02',
        default_args=default_args,
        start_date=datetime(2024, 2, 2, 2),
        schedule_interval='@daily'
)
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        first_name = 'Jerry'
        last_name = 'Fridman'
        return {
            'first_name': first_name,
            'last_name': last_name
        }
    
    @task()
    def get_age():
        age = 20
        return age
    
    @task()
    def greet(first_name, last_name, age):
        print(f'Hello, my name is {first_name} {last_name}.\n'
              f'I am {age} years old.')
    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'], 
          age=age)

greet_dag = hello_world_etl()
