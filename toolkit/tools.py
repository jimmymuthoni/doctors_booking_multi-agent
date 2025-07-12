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
    df = pd.read_csv("/home/brian/Documents/JIM/Doctor Appointment Multiagent/data/doctor_availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot_time'])

    if len(rows) == 0:
        output = "Doctor is not available for the entire day."
    else:
        output = f"This availability for {desired_date.date}\n"
        output += "Available slot: " + ', '.join(rows)
    return output


#function to check availabilty by specialiality
@tool
def check_availability_by_specialization(desired_date: Datemodel, specialization: Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    checking the database if we have the availability for the specific specialization.
    The prameters should be mentioned by user in the query
    """
    df = pd.read_csv("/home/brian/Documents/JIM/Doctor Appointment Multiagent/data/doctor_availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date) & (df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

    if len(rows) == 0:
        output = "No availabiliy in the entire day"
    else:
        def convert_to_am_pm(time_str):
            #split time string into hour and minutes
            time_str = str(time_str)
            hours, minutes = map(int, time_str.split(":"))
            period = 'AM' if hours < 12 else 'PM'
            #conveting hours to 12 -hour format
            hours = hours % 12 or 12
            return f"{hours}: {minutes:02d} {period}"
        output = f"This availability for {desired_date.date}\n"
        for row in rows.values:
            output += row[1] + ". Available slots: \n" + ', \n'.join([convert_to_am_pm(value) for value in row[2]])+'\n'

    return output


#function to make an appointment
@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    set apponintment or slot with the doctor.
    the parameters MUST be provided by the user in the query.
    """
    df = pd.read_csv("/home/brian/Documents/JIM/Doctor Appointment Multiagent/data/doctor_availability.csv")
    from datetime import datetime
    def convert_datetime_format(dt_str):
        dt = datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
        return dt.strftime("%d-%m-%Y %#H.%M")
    case = df[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]
    if len(case) == 0:
        return "No available appointments for that particular case."
    else:
        df.loc[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['doctor_name'] == doctor_name) & (df['is_available'] == True), ['is_available','patient_to_attend']] = [False, id_number.id]
        df.to_csv(f'availability.csv', index = False)

        return "Successfully done"

#function to cancel the appointmnet
@tool
def cancel_appointment(date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name: Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Cancelling doctor appointment.
    The paramaters should be provided by the user in the query
    """
    df = pd.read_csv("/home/brian/Documents/JIM/Doctor Appointment Multiagent/data/doctor_availability.csv")
    case_to_remove = df[(df['date_slot'] == date.date)&(df['patient_to_attend'] == id_number.id)&(df['doctor_name'] == doctor_name)]
    if len(case_to_remove) == 0:
        return "You don't have any appointment with that specification."
    else:
      df.loc[(df['date_slot'] == date.date) & (df['patient_to_attend'] == id_number.id) & (df['doctor_name'] == doctor_name), ['is_available', 'patient_to_attend']] = [True, None]
      df.to_csv(f'availability.csv', index = False)

      return "Successfully cancelled."








    
