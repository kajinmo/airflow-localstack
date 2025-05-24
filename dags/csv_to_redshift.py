from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
import pandas as pd

def ingest_csv_to_redshift():
    # Caminho do arquivo CSV dentro do container
    csv_path = '/opt/airflow/include/data/2025-05-04.csv'
    
    # Lê o CSV com parse de datas
    df = pd.read_csv(csv_path, parse_dates=['view_start_time', 'view_end_time'])
    
    # Conexão com o fake_redshift usando SQLAlchemy
    conn = BaseHook.get_connection('fake_redshift')
    uri = f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    engine = create_engine(uri)

    # Envia para o banco (substitui a tabela)
    df.to_sql('engagement_data', engine, index=False, if_exists='replace')
    print(f"Inseridos {len(df)} registros na tabela 'engagement_data'.")

with DAG(
    dag_id='csv_to_redshift',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    
    ingest_task = PythonOperator(
        task_id='ingest_csv_to_redshift',
        python_callable=ingest_csv_to_redshift
    )
