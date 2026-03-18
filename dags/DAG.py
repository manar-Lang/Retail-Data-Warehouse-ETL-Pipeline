from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
from sqlalchemy import create_engine

def run_retail_etl_process():
   
    path = '/opt/airflow/dags/'
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    df_list = []
    for f in files:
        file_full_path = os.path.join(path, f)
        df_list.append(pd.read_csv(file_full_path))

    if not df_list:
        raise Exception("No CSV files found to process!")

    
    df = pd.concat(df_list, ignore_index=True)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['quantity'] * df['unit_price']
    
    
    dim_customer = df[['customer_id', 'customer_name', 'city', 'country']].drop_duplicates()
    dim_product = df[['product_id', 'product_name', 'category', 'unit_price']].drop_duplicates()
    
    dim_date = pd.DataFrame({'order_date': df['order_date'].unique()})
    dim_date['year'] = dim_date['order_date'].dt.year
    dim_date['month'] = dim_date['order_date'].dt.month
    dim_date['day'] = dim_date['order_date'].dt.day
    
    fact_sales = df[['order_id', 'order_date', 'customer_id', 'product_id', 'quantity', 'total_revenue']]

    
    
    engine = create_engine('postgresql://airflow:airflow@postgres-airflow:5432/retail_dwh')
    
    dim_customer.to_sql('dim_customer', engine, if_exists='replace', index=False)
    dim_product.to_sql('dim_product', engine, if_exists='replace', index=False)
    dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)
    fact_sales.to_sql('fact_sales', engine, if_exists='replace', index=False)
    
    print("ETL Pipeline Finished Successfully!")


default_args = {
    'owner': 'Manar_ALtyp', 
    'start_date': datetime(2026, 3, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='Manar_Retail_Warehouse_Final', 
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id='build_retail_data_warehouse',
        python_callable=run_retail_etl_process
    )