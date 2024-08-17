import psycopg2
import os
from queries import *

class DatabaseManager:
    def __init__(self) -> None:
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            print("Database Connected ...")
        except Exception as e:
            print(f"ERROR : {e}")
            return
        self.cur = self.conn.cursor()

    def CreateTables(self):
        try:
            self.cur.execute(create_table_query)
            self.conn.commit()
            print("Tables Created ...\n")
        except Exception as e:
            print(f"ERROR : {e}")
        return
    
    def insert(self, tableName, values):
        if tableName == "CompanyData":
            insert_data_format = insert_data_CompanyData

        elif tableName == "EnrichedCompanyData":
            insert_data_format = insert_data_EnrichedCompanyData

        elif tableName == "similarOrganizations":
            insert_data_format = insert_data_similarOrganizations

        elif tableName == "affiliatedOrganizations":
            insert_data_format = insert_data_affiliatedOrganizations

        elif tableName == "location":
            insert_data_format = insert_data_location

        try:
            self.cur.executemany(insert_data_format, values)
            self.conn.commit()
        except Exception as e:
            print(f"ERROR in Insert : {e}")
            return
        print(f"\nValues(s) inserted to tabel {tableName} ...\n")
        return
    
    def delete_table(self, tableName):
        try:
            self.cur.execute(f"DROP TABLE {tableName} CASCADE")
            self.conn.commit()
            print(f"{tableName} deleted ...")
        except Exception as e:
            print(f"ERROR : {e}")
        return
    
    def showTabel(self, tabelName):
        if tabelName == "EnrichedComapanyData":
            query = show_enrichedCompanyData_table

        elif tabelName == 'EnrichedComapanyDatatabel':
            query = f"""SELECT * FROM EnrichedComapanyData"""

        else:
            query = f"""SELECT * FROM {tabelName}"""

        try:
            self.cur.execute(query)
            rows = self.cur.fetchall()
            print("\nData fetched ...\n")
        except Exception as e:
            print(f"ERROR : {e}")
            return
        return rows
    
    def close(self):
        self.cur.close()
        self.conn.close()
        print("Database Disconnected ...")
        return
