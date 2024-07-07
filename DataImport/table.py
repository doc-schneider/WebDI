from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import create_table, table_insert, add_columns


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
mycursor = conn.cursor()
#
db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)

# Create a table
table_dct = table_definitions[TableType.ALBUM]
create_table(db_engine, metadata, "albums", table_dct)

# Insert / add
table_insert(metadata, db_conn, "albums", album_table)

# Add foreign key column







