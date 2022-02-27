from pydantic import BaseModel, validator, Field
from datetime import date
from typing import List

class Genre(BaseModel):
	name: str

class Author(BaseModel) :
	first_name: str = Field(..., max_length=25)
	last_name: str
	age : int = Field(..., gt=15, lt=90, description="Age must be more than 15 and less than 90")
	@validator
	def check_age(cls, v):
		if v<15:
			raise ValueError('Age is less than 15')
		return v

class Book(BaseModel):
	title: str
	write: str
	duration: str
	date: date
	summary: str
	genres: List[Genre]
	pages: int