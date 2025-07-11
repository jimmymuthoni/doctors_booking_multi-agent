import pandas as pd
from langchain_core.tools import tool
from typing import Literal
from data_models.data_model import Datemodel, DateTimeModel, IdentificationNumberModel


#function to check doctors availability
@tool
def check_availability_by_doctor(desired_date: Datemodel, doctor_name: Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters shouls be mentioned by the user in the query.
    """
    df = pd.read_csv("data/doctor_availability.csv")

    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot_time'])

    if len(rows) == 0:
        output = "Doctor is not available for the entire day."
    else:
        output = f"This availability for {desired_date.date}\n"
        output += "Available slot: " + ', '.join(rows)
    return output



