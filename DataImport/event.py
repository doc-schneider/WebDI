import mysql.connector
import pandas as pd

from DataStructures.TableTypes import table_definitions, TableType
from DataStructures.Data import DataTable
from DataOperations.MySQL import table_insert_mysql, update_column, table_fetch_mysql


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
mycursor = conn.cursor()

# Add EVENT ID to another table based on event name
event_table = table_fetch_mysql(conn, "events")
# event_table = DataTable.fetch_table(TableType.EVENT, "events")
value_dct = event_table.set_index('EVENT')['ID_EVENT'].to_dict()
update_column(conn, mycursor, "photos", "ID_EVENT", "EVENT", value_dct)

# Add Event toe Event Table
cols = list(table_definitions[TableType.EVENT]["Columns"].keys())
foreign_key = table_definitions[TableType.EVENT]["ForeignKey"]
event_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: "Reise Berlin 2008",
        cols[1]: pd.Timestamp(2008, 4, 5, 8, 0, 0),
        cols[2]: pd.Timestamp(2008, 4, 7, 20, 0, 0),
        cols[3]: "",
        cols[4]: "Eine unserer vielen kleinen Reisen damals. Auch in der Reihe meiner damaligen Berlin-Begeisterung noch aus Unizeiten."
    }
)
# Potentially add foreign key (parent)
# event_table[foreign_key] = 2
# ...
table_insert_mysql(conn, mycursor, "events", event_table)

