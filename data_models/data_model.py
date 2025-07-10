import re
from pydantic import BaseModel, Field, field_validator

#class to verify datetime imputs from the user
class DateTimeModel(BaseModel):
    date: str = Field(description = "properly formated date", pattern = r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')
    @field_validator
    def check_date_format(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', v):
            raise ValueError ("The date should be in format: 'DD-MM-YYYY HH:MM'")
        return v
    
#class to verfy date
class Datemodel(BaseModel):
    date: str = Field(description = "Properly formatted date", pattern = r'^\d{2}-\d{2}-\d{4}$')
    @field_validator
    def check_date_format(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', v):
            raise ValueError("The date must be in the format:'DD-MM-YYYY'")
        return v
    
#class for verfying patient id
class IdentificationNumberModel(BaseModel):
    id: int = Field(description="Identification number 7 or 8 digits long")
    @field_validator
    def check_id_format(cls, v):
        if not re.match(r'^\d{7,8}$', str(v)): #convering strings before matching
            raise ValueError("The ID number should be a 7 or 8-digit number")
        return v
         