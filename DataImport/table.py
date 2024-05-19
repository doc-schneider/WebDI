from sqlalchemy import create_engine, MetaData

from DataStructures.TableTypes import TableType, table_types
from DataOperations.MySQL import create_table


db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)

# Create a table
table_dct = table_types[TableType.PHOTO]
create_table(db_engine, metadata, "photos", table_dct)


