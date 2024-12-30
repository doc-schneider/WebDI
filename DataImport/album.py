import pandas as pd
import mysql.connector

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from DataOperations.MySQL import table_fetch, table_fetch_mysql


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
mycursor = conn.cursor()

# Test
album_table = DataTable(table_fetch_mysql(conn, "albums"), TableType.ALBUM)
album_table.match_tag("Papas Kunst")







