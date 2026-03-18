# 🛒 Retail Data Warehouse ETL Pipeline

An end-to-end data engineering project that builds an automated ETL pipeline for retail sales data. The pipeline extracts data from CSV files, transforms it using Python and pandas, loads it into a PostgreSQL data warehouse, and orchestrates the entire workflow with Apache Airflow.

---

## 📌 Table of Contents

- [🔎 Project Overview](#-project-overview)
- [🏛 System Architecture](#-system-architecture)
- [📊 Data Model (Star Schema)](#-data-model-star-schema)
- [🚀 Final Goals](#-final-goals)
- [⚙️ Prerequisites](#️-prerequisites)
- [🚀 Quick Start](#-quick-start)
- [📦 Docker Setup](#-docker-setup)
- [🧪 ETL Pipeline Details](#-etl-pipeline-details)
- [📊 Power BI Dashboard](#-power-bi-dashboard)
- [🧪 Testing & Validation](#-testing--validation)
- [🗂 Directory Structure](#-directory-structure)
- [📦 Tech Stack](#-tech-stack)
- [🐛 Troubleshooting](#-troubleshooting)
- [🧾 License](#-license)
- [👨‍💻 Author](#-author)


---

## 🔎 Project Overview

This project implements a complete **ETL (Extract, Transform, Load) pipeline** for retail sales data. It automates the process of extracting monthly sales data from CSV files, cleaning and transforming it using Python/Pandas, and loading it into a PostgreSQL Data Warehouse using a **Star Schema design**, all orchestrated by **Apache Airflow**.

### **Business Value**
- 📈 Enable data-driven decision making with clean, structured retail data
- 🔄 Automate manual data processing workflows
- 📊 Provide a foundation for business intelligence and analytics
- 🎯 Track key metrics: revenue, orders, customer behavior, product performance

---

## 🏛 System Architecture

The pipeline follows a modern data engineering architecture:

1. **Extract Layer**: Reads raw monthly sales data from CSV files in the `/opt/airflow/data/` directory
2. **Transform Layer**: 
   - Data cleaning and standardization
   - Feature engineering (calculating `total_revenue = quantity × unit_price`)
   - Data modeling (splitting data into Dimensions and Fact tables)
3. **Load Layer**: Upserts the final structured data into PostgreSQL database named `retail_dwh`
4. **Orchestration Layer**: Managed by Apache Airflow for automated scheduling and monitoring
5. **Visualization Layer**: Power BI dashboards connected to the data warehouse for business intelligence

---

## 📊 Data Model (Star Schema)

The warehouse is designed for high-performance analytical queries following the **Kimball dimensional modeling** approach:

### **Fact Table**
| Table | Description | Metrics |
|-------|-------------|---------|
| `fact_sales` | Transaction-level sales data | quantity, total_revenue |

### **Dimension Tables**
| Table | Description | Attributes |
|-------|-------------|------------|
| `dim_customer` | Customer profiles | customer_id, customer_name, city, country |
| `dim_product` | Product information | product_id, product_name, category, unit_price |
| `dim_date` | Time attributes | order_date, year, month, day |

### **Schema Diagram**
```
┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│ dim_customer │────▶│                │◀────│  dim_product │
│              │     │   fact_sales   │     │              │
│  customer_id │◀────│                │────▶│  product_id  │
└──────────────┘     │   order_id     │     └──────────────┘
                     │   quantity     │            ▲
┌──────────────┐     │ total_revenue  │            │
│   dim_date   │────▶│   order_date   │────────────┘
│  order_date  │◀────└────────────────┘
│    year      │
│    month     │
│    day       │
└──────────────┘
```

---

## 🚀 Final Goals

- ✅ **Automated ETL Pipeline**: Extract CSV files, transform with pandas, load to PostgreSQL
- ✅ **Star Schema Design**: Implement fact and dimension tables for analytics
- ✅ **Airflow Orchestration**: Schedule and monitor pipeline execution
- ✅ **Data Quality**: Clean and validate data during transformation
- ✅ **Docker Environment**: Fully containerized with pre-configured services
- ✅ **Power BI Integration**: Connect data warehouse to visualization tools
- ✅ **Comprehensive Documentation**: Clear setup and usage instructions

---

## ⚙️ Prerequisites

### **Software Required**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)
- [Git](https://git-scm.com/)
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (for visualization)
- 8GB+ RAM recommended

### **Required Skills**
- Basic SQL
- Python fundamentals
- Understanding of ETL concepts
- Familiarity with Airflow (helpful but not required)

---

## 🚀 Quick Start

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/manar-Lang/retail-data-warehouse-etl.git
cd retail-data-warehouse-etl
```

### **Step 2: Start Docker Containers**
```bash
docker-compose up -d
```

This starts:
- Airflow Webserver & Scheduler (port 8080)
- PostgreSQL for Airflow metadata (port 5432)
- PostgreSQL for Data Warehouse (port 5433)
- pgAdmin (port 5050)

### **Step 3: Initialize Database**
The database is automatically initialized with:
```bash
# The init-db.sql script runs automatically on first container start
# It creates the retail_dwh database
```

### **Step 4: Place CSV Files**
Copy your monthly sales CSV files to the data directory:
```bash
cp your-sales-data/*.csv data/
```

### **Step 5: Access Airflow UI**
- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

### **Step 6: Trigger the DAG**
1. In Airflow UI, find the DAG `Manar_Retail_Warehouse_V1`
2. Click the "Play" button to trigger
3. Monitor execution in the "Graph" view

### **Step 7: Verify in pgAdmin**
- URL: http://localhost:5050
- Email: `admin@example.com`
- Password: `admin`
- Connect to PostgreSQL server and query the tables

### **Step 8: Connect Power BI**
1. Open Power BI Desktop
2. Get Data → PostgreSQL Database
3. Server: `localhost` (or container IP)
4. Database: `retail_dwh`
5. Import tables or use DirectQuery

---

## 📦 Docker Setup

### **Services Configuration**

| Service | Purpose | Port | Credentials |
|---------|---------|------|-------------|
| `postgres-airflow` | Airflow metadata DB | 5432 | airflow/airflow |
| `postgres-app` | Data warehouse (retail_dwh) | 5433 | airflow/airflow |
| `airflow-webserver` | Airflow UI | 8080 | airflow/airflow |
| `airflow-scheduler` | DAG scheduler | - | - |
| `pgadmin` | Database management | 5050 | admin@example.com/admin |

### **Volume Mappings**
```yaml
volumes:
  - ./dags:/opt/airflow/dags          # DAG files
  - ./logs:/opt/airflow/logs          # Airflow logs  
  - ./data:/opt/airflow/data          # Source CSV files
  - ./include:/opt/airflow/include    # Helper scripts
  - ./postgres/init:/docker-entrypoint-initdb.d  # DB init scripts
```

### **Database Initialization Script**
The `postgres/init/init-db.sql` script runs automatically:
```sql
-- Create the retail data warehouse database
CREATE DATABASE retail_dwh;
```

---

## 🧪 ETL Pipeline Details

### **DAG: Manar_Retail_Warehouse_V1**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
from sqlalchemy import create_engine

def run_retail_etl_process():
    path = '/opt/airflow/data/'
    engine = create_engine('postgresql://airflow:airflow@postgres-app:5432/retail_dwh')
    
    # Extract
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    df_list = []
    for f in files:
        file_full_path = os.path.join(path, f)
        df_list.append(pd.read_csv(file_full_path))
    
    if not df_list:
        raise Exception("No CSV files found to process!")
    
    df = pd.concat(df_list, ignore_index=True)
    
    # Transform
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['quantity'] * df['unit_price']
    
    # Create dimensions
    dim_customer = df[['customer_id', 'customer_name', 'city', 'country']].drop_duplicates()
    dim_product = df[['product_id', 'product_name', 'category', 'unit_price']].drop_duplicates()
    
    dim_date = pd.DataFrame({'order_date': df['order_date'].unique()})
    dim_date['year'] = dim_date['order_date'].dt.year
    dim_date['month'] = dim_date['order_date'].dt.month
    dim_date['day'] = dim_date['order_date'].dt.day
    
    # Create fact
    fact_sales = df[['order_id', 'order_date', 'customer_id', 'product_id', 'quantity', 'total_revenue']]
    
    # Load
    dim_customer.to_sql('dim_customer', engine, if_exists='replace', index=False)
    dim_product.to_sql('dim_product', engine, if_exists='replace', index=False)
    dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)
    fact_sales.to_sql('fact_sales', engine, if_exists='replace', index=False)
    
    print("Retail ETL Pipeline Task Completed Successfully!")

default_args = {
    'owner': 'Manar_ALtyp',
    'start_date': datetime(2026, 3, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='Manar_Retail_Warehouse_V1',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id='run_retail_etl',
        python_callable=run_retail_etl_process
    )
```

### **DAG Features**
- **Schedule**: `@daily` - runs once per day at midnight
- **Retries**: 1 retry with 5-minute delay on failure
- **Owner**: Manar_ALtyp
- **Catchup**: False (doesn't backfill missed runs)
- **Task**: Single PythonOperator executing the ETL logic

---

## 📊 Power BI Dashboard

### **Key Visuals**

| Visual | Purpose | Business Question |
|--------|---------|-------------------|
| **KPI Cards** | Total Revenue, Orders, AOV | How are we performing overall? |
| **Donut Chart** | Revenue by Category | Which product categories drive revenue? |
| **Line Chart** | Monthly Revenue Trend | Is revenue growing over time? |
| **Gauge Chart** | Performance vs 20% Target | Are we meeting growth targets? |
| **Map Visual** | Revenue by City/Country | Where are our top markets? |
| **Decomposition Tree** | Root Cause Analysis | Why did revenue change? |

### **DAX Measures**
```dax
Total Revenue = SUM(fact_sales[total_revenue])
Total Orders = DISTINCTCOUNT(fact_sales[order_id])
Average Order Value = [Total Revenue] / [Total Orders]
Revenue Growth % = 
    VAR CurrentRevenue = [Total Revenue]
    VAR PreviousRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[order_date]))
    RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0)
```

---

## 🧪 Testing & Validation

### **Verify Table Creation**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
-- Expected: dim_customer, dim_product, dim_date, fact_sales
```

### **Check Row Counts**
```sql
SELECT 'fact_sales' as table_name, COUNT(*) as row_count FROM fact_sales
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date;
```

### **Verify Referential Integrity**
```sql
-- Check for orphaned records
SELECT COUNT(*) as orphaned_sales
FROM fact_sales f
LEFT JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

### **Test Data Quality**
```sql
-- Check for nulls in key fields
SELECT 
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_orders,
    SUM(CASE WHEN total_revenue IS NULL THEN 1 ELSE 0 END) as null_revenue
FROM fact_sales;
```

---

## 🗂 Directory Structure

```
retail-data-warehouse-etl/
│
├── README.md                          # Project documentation
├── docker-compose.yml                  # Docker services configuration
├── .env                                # Environment variables
├── .gitignore                          # Git ignore rules
│
├── dags/
│   ├── retail_etl_dag.py               # Main Airflow DAG
│   └── __init__.py
│
├── data/
│   ├── sales_jan2025.csv               # Monthly sales data
│   ├── sales_feb2025.csv
│   └── README.md                        # CSV format instructions
│
├── include/
│   └── etl_helpers.py                   # Shared ETL functions (optional)
│
├── postgres/
│   └── init/
│       └── init-db.sql                   # DB initialization script
│
├── logs/                                 # Airflow logs (auto-generated)
├── config/                               # Airflow config (if needed)
├── plugins/                              # Custom Airflow plugins
│
├── power_bi/
│   ├── retail_dashboard.pbix              # Power BI dashboard
│   └── screenshots/
│       ├── overview.png
│       ├── revenue_by_category.png
│       └── decomposition_tree.png
│
├── scripts/
│   ├── generate_test_data.py              # Script to create sample CSVs
│   └── validate_warehouse.sql             # Validation queries
│
├── notebooks/
│   ├── 01_data_exploration.ipynb          # EDA notebook
│   └── 02_etl_development.ipynb           # ETL prototyping
│
├── docs/
│   ├── architecture_diagram.png
│   ├── data_flow_diagram.png
│   ├── star_schema.png
│   └── deployment_guide.md
│
└── outputs/
    ├── etl_logs.txt
    └── validation_results.csv
```

---

## 📦 Tech Stack

| Category             | Tool/Library                | Purpose                               |
|----------------------|----------------------------|---------------------------------------|
| **Orchestration**    | Apache Airflow v2.7.3       | Workflow automation and scheduling    |
| **Processing**       | Python 3.8+                 | Core ETL logic                        |
| **Data Processing**  | pandas                      | Data manipulation and transformation  |
| **Database**         | PostgreSQL                  | Data warehouse storage                |
| **Database Toolkit** | SQLAlchemy                  | Database connections and operations   |
| **Environment**      | Docker & Docker-Compose     | Containerization and service orchestration |
| **Visualization**    | Power BI                    | Business intelligence dashboards      |
| **Database Mgmt**    | pgAdmin                     | PostgreSQL management interface       |
| **Development**      | Jupyter Notebooks           | Exploration and prototyping           |
| **Version Control**  | Git + GitHub                | Code management                       |

**Key Dependencies:**
```txt
pandas>=1.5.0
sqlalchemy>=1.4.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Cannot connect to Airflow UI** | Run `docker-compose restart` and wait 2 minutes |
| **No CSV files found** | Ensure files are in `./data/` directory with `.csv` extension |
| **Database "retail_dwh" not found** | Check `postgres/init/init-db.sql` ran correctly |
| **Permission denied** | Run `chmod -R 777 ./logs ./data` |
| **Port already in use** | Change ports in `docker-compose.yml` |
| **DAG not appearing in UI** | Check file is in `./dags/` and has no syntax errors |
| **Connection refused to PostgreSQL** | Verify container is running: `docker ps` |
| **ERR_EMPTY_RESPONSE** | Perform clean restart: `docker-compose down -v && docker-compose up -d` |

---

## 🧾 License

No license has been selected for this project yet.
All rights reserved — you may not use, copy, modify, or distribute this code without explicit permission from the author.

---

## 👨‍💻 Author

**Manar Altyp**  
*Data Engineer • ETL Specialist • BI Developer*

🌐 [GitHub](https://github.com/manar-Lang) 

*Project completed for: Retail Data Warehouse ETL Pipeline*  
*Completion Date: March 2026*

---

