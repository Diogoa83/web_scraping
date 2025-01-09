import sys
sys.path.append('/opt/airflow/dags/SINAN/sinan_desenvolvimento/web_scraping')

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from emails import emails_notificacao_airflow
#from main import codigo_main
#from extrair_zip import extrair_zip
#from carga_tabela_temp_dengue_chikungunya import cargar_tabela_temp_sinan

default_args = {
    'owner': 'Dag_Chikon_Dengon',
    'depends_on_past': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=40),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': emails_notificacao_airflow,
    'sla': timedelta(minutes=130)
}

dag = DAG(
    'Dag_Chikon_Dengon',
    default_args=default_args,
    start_date=datetime(2024, 8, 27),
    tags=['sinan', 'chikon', 'dengon'],
    description='Sinan',
    schedule_interval='0 5 * * *',
    catchup=False,
)



main_task = BashOperator(
    task_id='main_task',
    bash_command="python /opt/airflow/dags/SINAN/sinan_desenvolvimento/web_scraping/main.py",  
    dag=dag,)

extrair_zip_task = BashOperator(
    task_id='extrair_zip_task',
    bash_command="python /opt/airflow/dags/SINAN/sinan_desenvolvimento/web_scraping/extrair_zip.py",
    dag=dag
)

# extrair_zip_task = PythonOperator(
#     task_id='extrair_zip_task',
#     python_callable=extrair_zip,  
#     dag=dag
# )

carga_tabela_temp_task = BashOperator(
    task_id='carga_tabela_temp_task',
    bash_command="python /opt/airflow/dags/SINAN/sinan_desenvolvimento/web_scraping/carga_tabela_temp_dengue_chikungunya.py",
    dag=dag
)

# carga_tabela_temp_task = PythonOperator(
#     task_id='carga_tabela_temp_task',
#     python_callable=cargar_tabela_temp_sinan,  
#     dag=dag
# )


tratados_task = BashOperator(
    task_id='tratados_task',
    bash_command="sinankjb.sh",
    dag=dag
)


main_task >> extrair_zip_task >> carga_tabela_temp_task >> tratados_task




