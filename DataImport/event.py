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

# Add Event to Event Table
cols = list(table_definitions[TableType.EVENT]["Columns"].keys())
foreign_key = table_definitions[TableType.EVENT]["ForeignKey"]
event_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: "Reise nach Indien 2024",
        cols[1]: events_dct["Anreise"]["DATE_FROM"],
        cols[2]: events_dct["Delhi Abreise"]["DATE_TO"],
        cols[3]: "",
        cols[4]: "Indien war Teil meines Welt-Reiseplans. Alle wichtigen Kulturräume der Welt. Zum Glück hatte Konstanze irgendwann umgeschwenkt von Ablehnung zu Interesse. Das Indien eine eigene Welt ist, ist richtig."
    }
)
# Potentially add foreign key (parent)
# event_table[foreign_key] = 2
# ...
table_insert_mysql(conn, mycursor, "events", event_table)

