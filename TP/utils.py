import os
import platform
import pyodbc
import pandas as pd
import sqlalchemy


SQL_DIRPATH_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "./sql/"))
assert os.path.isdir(SQL_DIRPATH_), f'El directorio "{SQL_DIRPATH_}" no existe.'

PLOTS_DIRPATH_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "./graficos/"))
assert os.path.isdir(PLOTS_DIRPATH_), f'El directorio "{PLOTS_DIRPATH_}" no existe.'


class SQLConnection:
    # Datos de conexión
    driver_windows = "{ODBC Driver 17 for SQL Server}"
    driver_ubuntu = "ODBC Driver 18 for SQL Server"
    server = "157.92.26.17,1443"  # IP y puerto
    database = "AdventureWorks2019"
    username = "Alumno"
    password = "mrcd2025"

    def __init__(self):
        is_windows = platform.system() == "Windows"
        self.driver_ = self.driver_windows if is_windows else self.driver_ubuntu
        self.conn = None
        self.engine = None
        self.create()

    def create(self):
        conn_str = (
            f"DRIVER={self.driver_};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=yes;"
        )
        conn_url = sqlalchemy.engine.URL.create(
            "mssql+pyodbc", query={"odbc_connect": conn_str}
        )
        self.engine = sqlalchemy.create_engine(conn_url)

    def run_query(self, sql_fn):
        fp = os.path.join(SQL_DIRPATH_, sql_fn)
        assert os.path.isfile(fp), f'El archivo "{fp}" no existe.'
        with open(fp, "r", encoding="utf-8") as f:
            query = f.read()
        query = sqlalchemy.text(query)  # Convertir a objeto de texto SQLAlchemy
        with self.engine.begin() as conn:
            return pd.read_sql_query(query, conn)

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Conexión cerrada.")
        else:
            print("No hay conexión para cerrar.")


if __name__ == "__main__":
    try:
        sql_conn = SQLConnection()
        cursor = sql_conn.conn.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        if row:
            print("-" * 10)
            print("SQL Server version:\n", row[0])
            print("-" * 10)
    except Exception as e:
        raise e
