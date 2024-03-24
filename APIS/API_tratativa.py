import os
import pandas as pd
import psycopg2
from psycopg2 import sql

def create_table(cur):
    table_name = 'Tratativa_TB'
    columns = [
        'unique_id',
        'spx_tracking_number',
        'exception_order_id',
        'operate_time',
        'operator',
        'station',
        'operation',
        'event',
        'eo_status',
        'status_final',
        'status_definitivo_v',
        'data', 
        'turno',
        'hora_cheia',
        'tempo_medio_pacote' 
    ]
    
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            unique_id VARCHAR PRIMARY KEY,
            {', '.join([f'"{column}" VARCHAR' for column in columns[1:]])},
            UNIQUE (unique_id)  -- Adiciona restrição de unicidade na coluna unique_id
        )
    """
    cur.execute(create_table_query)


def extract_status_definitivo(operation_text):
    if ":" in operation_text:
        return operation_text.split(":", 1)[1].strip()
    else:
        return None 

def extract_status_final(operation_text):
    if ":" in operation_text:
        return operation_text.split(":", 1)[0].strip()
    else:
        return None  

def calcular_turno(operate_time):
    if operate_time.hour >= 5 and operate_time.hour < 13:
        return 'T1'
    elif operate_time.hour >= 14 and operate_time.hour < 22:
        return 'T2'
    else:
        return 'T3'

def calcular_tempo_medio_pacote(spx_tracking_number, status_final, operate_time, df):
    if status_final == 'Inbound':
        resolve_time = df[(df['spx_tracking_number'] == spx_tracking_number) & (df['status_final'] == 'Resolve')]['operate_time'].values
        if len(resolve_time) > 0:
            tempo_medio = max((resolve_time[0] - operate_time).total_seconds() /60, 0)
            return float(tempo_medio)
    return "9999999"

def formatar_data_hora(data_str):
    return pd.to_datetime(data_str, format='%Y%m%d%H%M%S', errors='coerce')

def consolidate_csv_files(csv_directory, db_params):
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]
    
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    create_table(cur)

    dados = [] 

    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(csv_directory, csv_file), skiprows=1, names=[
            'spx_tracking_number',
            'exception_order_id',
            'operate_time',
            'operator',
            'station',
            'operation',
            'event',
            'eo_status'
        ])

      
        df['operate_time'] = pd.to_datetime(df['operate_time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        df = df.dropna(subset=['operate_time'])

        df['data'] = df['operate_time'].dt.strftime('%Y-%m-%d')
        df['hora_cheia'] = df['operate_time'].dt.strftime('%H:00:00')

        df['status_final'] = df['operation'].apply(extract_status_final)
        df['status_definitivo_v'] = df['operation'].apply(extract_status_definitivo)

        df['turno'] = df['operate_time'].apply(calcular_turno)

        df['tempo_medio_pacote'] = df.apply(lambda row: calcular_tempo_medio_pacote(row['spx_tracking_number'], row['status_final'], row['operate_time'], df), axis=1)

        df['unique_id'] = df['spx_tracking_number'] + '_' + df['exception_order_id'].astype(str) + '_' + df['operate_time'].astype(str)

        dados.extend(df[['unique_id', 'spx_tracking_number', 'exception_order_id', 'operate_time', 'operator', 'station', 'operation', 'event', 'eo_status', 'status_final', 'status_definitivo_v', 'data', 'turno', 'hora_cheia', 'tempo_medio_pacote']].values)

    print('Subindos os dados')

    print(dados)
    insert_query = sql.SQL("""
        INSERT INTO Tratativa_TB (unique_id, spx_tracking_number, exception_order_id, operate_time, operator, station, operation, event, eo_status, status_final, status_definitivo_v, data, turno, hora_cheia, tempo_medio_pacote)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (unique_id) DO NOTHING
    """)
    cur.executemany(insert_query, dados)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    csv_directory = "C:\\Users\\Seagroup\\Documents\\Humberto\\TO Tratativas"

    db_params = {
        "dbname": "humberto_projects",
        "user": "postgres",
        "password": "Masterkey30010069.",
        "host": "140.238.185.16",
        "port": "15432"
    }

    consolidate_csv_files(csv_directory, db_params)
