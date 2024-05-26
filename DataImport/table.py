from sqlalchemy import create_engine, MetaData, insert

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import create_table


db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)

# Create a table
table_dct = table_definitions[TableType.PHOTO]
create_table(db_engine, metadata, "photos", table_dct)

# Insert / add
query = insert(metadata.tables["photos"])
Result = db_conn.execute(query, photo_table.table.to_dict(orient='records'))
db_conn.commit()


