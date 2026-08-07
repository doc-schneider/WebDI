from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from DataOperations.Helper import get_pretable, parse_liststring
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config

config.environment_storage = "LOCAL"
initialize_MySQL()

# For the Join Tables
keys_tables = {"ID_NOTE": "notes", "ID_DOCUMENT": "documents"}


biography = "Mama"

biography_table_file = Path("W:/Biographie/Mama/TABLES/Biographie/Biograpy_Mama.csv")
biography_table_raw, _, _, _ = get_pretable(biography_table_file, [])

reference_tables = list(set(biography_table_raw.columns) - set(table_definitions[TableType.BIOGRAPHY_SECTION]["Columns"].keys()))
biography_section_table = biography_table_raw.drop(columns=reference_tables)
biography_section_table["BIOGRAPHY"] = biography
biography_section_table = DataTable(biography_section_table, TableType.BIOGRAPHY_SECTION)

flag_biography_table = False
if flag_biography_table:
    biography_table = pd.DataFrame(
        index=[0],
        data={
            "BIOGRAPHY": biography,
            "DESCRIPTION": "Mamas Biografie",
            "OWNER": "Mama",
            "TITLE": ""  # TODO Remove Title
        }
    )
    table_insert(config.mysql["metadata"], config.mysql["conn"], "biographies", biography_table)

biography_section_table.add_foreignkey("BIOGRAPHY", "biographies", TableType.BIOGRAPHY)
# Insert the new sections
#table_insert(config.mysql["metadata"], config.mysql["conn"], "biography_sections", biography_section_table.table)

# Update Join Table
# TODO This only works if TITLE unique. I need the IDs better in the step before already
biography_table_raw['ID_BIOGRAPHY_SECTION'] = biography_table_raw['TITLE'].map(
    DataTable.fetch_table(
        TableType.BIOGRAPHY_SECTION,
        "biography_sections"
    ).table.set_index('TITLE')['ID_BIOGRAPHY_SECTION']
)
for ref_id in reference_tables:
    biography_section_jointable = biography_table_raw[['ID_BIOGRAPHY_SECTION']].copy()
    for row in biography_table_raw[["ID_BIOGRAPHY_SECTION", ref_id]].itertuples():
        lst_id = parse_liststring(row[2])
        biography_section_jointable = biography_section_jointable.merge(
            pd.DataFrame(
                data={"ID_BIOGRAPHY_SECTION": row[1], ref_id: lst_id}
            ),
            on="ID_BIOGRAPHY_SECTION",
            how="left"
        )
    table_insert(
        config.mysql["metadata"],
        config.mysql["conn"],
        "biography_sections_jointable_" + keys_tables[ref_id],
        biography_section_jointable
    )



