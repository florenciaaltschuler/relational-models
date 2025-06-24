import os
import platform
import pandas as pd
import sqlalchemy


SQL_DIRPATH_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "./SQL2/"))
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

    def run_query(self, query: str) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL y devuelve el resultado como un pd.DataFrame.
        """
        assert self.engine is not None, "Error: No se creó la conexión."
        # Convertir a objeto de texto SQLAlchemy
        query = sqlalchemy.text(query)
        with self.engine.begin() as conn:
            return pd.read_sql_query(query, conn)

    def run_sql_file(self, sql_fn: str) -> pd.DataFrame:
        """
        Ejectuta una consulta SQL a partir de un archivo .sql y
        devuelve el resultado como un pd.DataFrame.
        """
        fp = os.path.join(SQL_DIRPATH_, sql_fn)
        assert os.path.isfile(fp), f'El archivo "{fp}" no existe.'
        with open(fp, "r", encoding="utf-8") as f:
            query = f.read()
        return self.run_query(query)

    def close(self):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None


if __name__ == "__main__":
    sql_conn = SQLConnection()
    df = sql_conn.run_query("SELECT @@version as version;")
    assert len(df) == 1, f"Se devolvieron {len(df)} filas cuando se esperaba 1."
    sql_ver = df["version"][0]
    print("-"*10)
    print(sql_ver)
    print("-"*10)
