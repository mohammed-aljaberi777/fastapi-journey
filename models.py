
from pydantic import BaseModel,Field,model_validator
from typing import List,Optional
from datetime import date







#gear second 
class BorrowRecord(BaseModel):
   borrower_name: str = Field(min_length=2, max_length=50)
   borrow_date: date
   return_date: Optional[date] = None
  


# primary en
class Book(BaseModel):
  id : int = Field(gt=0)
  title : str = Field(min_length = 2, max_lengeth =50)
  author : str = Field(min_length = 2, max_lengeth =50)
  year : int = Field(ge=1940,le=2026)
  copies : int = Field(ge=1)
  borrow_records: List[BorrowRecord] = []


  @model_validator(mode="after")
  def check_year_not_future(self):
    if self.year > 2026:
      raise ValueError("year can not beee in the future")
    return self 







