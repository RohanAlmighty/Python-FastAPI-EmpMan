from fastapi import FastAPI, status, Path, HTTPException, Depends
from pydantic import BaseModel, Field, StrictInt, StrictStr
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated

from database import engine, SessionLocal
from models import Base, Employees

# from employees import EMPLOYEES

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class EmployeeRequest(BaseModel):
    e_id: Optional[StrictInt] = Field(gt=0, default=None)
    e_name: StrictStr = Field(min_length=3)
    e_pos: StrictStr = Field(min_length=3)
    e_sal: StrictInt = Field(gt=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "e_name": "Employee Name",
                "e_pos": "Employee Position",
                "e_sal": 10000,
            },
        }


class EmployeeResponse(BaseModel):
    e_id: StrictInt = Field(gt=0)
    e_name: StrictStr = Field(min_length=3)
    e_pos: StrictStr = Field(min_length=3)
    e_sal: StrictInt = Field(gt=1000)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "e_id": 1,
                "e_name": "Employee Name",
                "e_pos": "Employee Position",
                "e_sal": 10000,
            },
        }


@app.get(
    "/emp/",
    status_code=status.HTTP_200_OK,
    response_model=List[EmployeeResponse],
)
async def get_all_employees(
    db: db_dependency,
):
    return db.query(Employees).all()


@app.get(
    "/emp/{e_id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponse,
)
async def get_employee_by_id(
    db: db_dependency,
    e_id: StrictInt = Path(gt=0),
):
    employee_model = db.query(Employees).filter(Employees.e_id == e_id).first()
    if not employee_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee_model


@app.post(
    "/emp/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponse,
)
async def create_new_employee(
    db: db_dependency,
    emp: EmployeeRequest,
):
    employee_request = Employees(**(emp.model_dump()))
    if (
        employee_request.e_id
        and db.query(Employees)
        .filter(Employees.e_id == employee_request.e_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee id already exists",
        )
    db.add(employee_request)
    db.commit()
    db.refresh(employee_request)
    return EmployeeResponse.model_validate(employee_request)


@app.put(
    "/emp/{e_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_employee(
    db: db_dependency,
    emp: EmployeeRequest,
    e_id: StrictInt = Path(gt=0),
):
    employee_request = Employees(**(emp.model_dump()))
    employee_model = db.query(Employees).filter(Employees.e_id == e_id).first()
    if employee_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    employee_model.e_name = employee_request.e_name
    employee_model.e_pos = employee_request.e_pos
    employee_model.e_sal = employee_request.e_sal
    db.add(employee_model)
    db.commit()


@app.delete(
    "/emp/{e_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    db: db_dependency,
    e_id: StrictInt = Path(gt=0),
):
    employee_model = db.query(Employees).filter(Employees.e_id == e_id).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.query(Employees).filter(Employees.e_id == e_id).delete()
    db.commit()
