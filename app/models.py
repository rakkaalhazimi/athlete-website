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
    DoB: str
    Sex: str
    Current_Club: str
    Current_City: str
    Current_Province: str
    # Achievment: List[Achievments]
    # Current_School: str
    # NISNAS: str


# All athelte fields
athlete_fields = [field.name for field in fields(Athletes)]
achievment_fields = [field.name for field in fields(Achievments)]
    

if __name__ == "__main__":
    cols = fields(Achievments)
    for col in cols:
        print(col.name)