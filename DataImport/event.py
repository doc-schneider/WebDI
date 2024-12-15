import mysql.connector
import pandas as pd

from DataStructures.TableTypes import table_definitions, TableType
from DataOperations.MySQL import table_insert_mysql


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
mycursor = conn.cursor()

cols = list(table_definitions[TableType.EVENT]["Columns"].keys())
foreign_key = table_definitions[TableType.EVENT]["ForeignKey"]
event_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: "Wohnung streichen 2024",
        cols[1]: pd.Timestamp(2024, 11, 18, 8, 0, 0),
        cols[2]: pd.Timestamp(2024, 11, 28, 15, 0, 0),
        cols[3]: "",
        cols[4]: "Seit Jahren brennen mir schon die schimmligen Fensterfugen auf den Nägeln. Dafür kommt aber kein Handwerker. Also verbinden wir das mit einem neuen Anstrich und Lackierungen der Wohnung. Das ist sowieso überfällig. Damit haben wir dann hoffentlich Ruhe bis zum Ende"
    }
)
# Potentially add foreign key
# ...
table_insert_mysql(conn, mycursor, "events", event_table)
