from sqlalchemy import create_engine, MetaData
from pathlib import Path

from DataOperations.Photo import PhotoFactory


photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2022/2022_07_Lofoten/Auswahl/0_Flug"),
        Path("Y:/2022/2022_07_Lofoten/Auswahl/1_Tromsö"),
        Path("Y:/2022/2022_07_Lofoten/Auswahl/2_Lyngen Alpen_Setermoen"),
        Path("Y:/2022/2022_07_Lofoten/Auswahl/3_Svolvaer"),
        Path("Y:/2022/2022_07_Lofoten/Auswahl/4_Reine"),
        Path("Y:/2022/2022_07_Lofoten/Auswahl/5_Rückfahrt"),
    ],
    "Reise Nord-Norwegen 2022",
    [
        "Flug",
        "Tromsö",
        "Lyngen Alpen_Setermoen",
        "Svolvaer",
        "Reine",
        "Rückfahrt"
    ],
    Path("Y:/2022/2022_07_Lofoten/Auswahl/Pre-Dokumentliste.csv")
)

print("done")



