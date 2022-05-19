from typing import Any, List
from dataclasses import dataclass, fields


@dataclass
class Achievments:
    Rnk: Any
    Meet_ID: Any
    Besttime: Any
    FP: Any
    R1_rate: Any
    R2_rate: Any
    R3_rate: Any
    Event_ID: str
    Event_Description: str
    Kind: str
    Date: str
    Place: str

@dataclass
class Athletes:
    Athlete_ID: int
    Athlete_Name: str
    NISNAS: str
    DoB: str
    Sex: str
    Level: str
    Current_School: str
    Current_Club: str
    Current_City: str
    Current_Province: str
    Achievment: List


@dataclass
class AthletesShow:
    Athlete_ID: int
    Athlete_Name: str
    DoB: str
    Sex: str
    Current_Club: str
    Current_City: str
    Current_Province: str

@dataclass
class AthletesSearch:
    Athlete_Name: str
    Current_Club: str
    Current_City: str
    Current_Province: str


def create_fields(dclass):
    return [field.name for field in fields(dclass)]


# All fields
athlete_fields = create_fields(Athletes)
athlete_show_fields = create_fields(AthletesShow)
athlete_search_fields = create_fields(AthletesSearch)
achievment_fields = create_fields(Achievments)
    

if __name__ == "__main__":
    cols = fields(Achievments)
    for col in cols:
        print(col.name)