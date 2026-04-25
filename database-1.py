#import needed libraries
from sqlalchemy import create_engine
import pyodbc
import pandas as pd
import os

#get password from environmnet var
pwd = os.environ['PGPASS']
uid = os.environ['PGUID']
server = "localhost"
db = "postgres"
port = "5432"


#extract data from sql server
def extract():
    try:
        directory = r'C:\Users\SVatsa\OneDrive - Generac Power Systems, Inc\Vatsa\Work Directory\Projects\GaN'
        filename = 'GaN Inverter BOM_Elec.xlsx'
        file_wo_ext = 'GaN Inverter BOM_Elec'

        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            df_data = pd.read_excel(f)
            load(df_data, file_wo_ext)

    except Exception as e:
        print("Data extract error: " + str(e))

#load data to postgres
def load(df1, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{db}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df1)}... ')

        # save df to postgres
        df1.to_sql(f"stg_{tbl}", engine, if_exists='replace', index=False)
        rows_imported += len(df1)

        # add elapsed time to final print out
        print("Data imported successful")

    except Exception as e:
        print("Data load error: " + str(e))

try:
    #call extract function
    df = extract()
except Exception as e:
    print("Error while extracting data: " + str(e))

