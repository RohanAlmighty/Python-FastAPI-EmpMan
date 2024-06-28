from pydantic import BaseModel, Field, StrictInt, StrictStr


class Employee(BaseModel):
    e_id: StrictInt = Field(gt=0)
    e_name: StrictStr = Field(min_length=3)
    e_pos: StrictStr = Field(min_length=3)
    e_sal: StrictInt = Field(gt=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "e_id": 1,
                "e_name": "Employee Name",
                "e_pos": "Employee Position",
                "e_sal": 10000,
            },
        }


EMPLOYEES = [
    Employee(
        e_id=1,
        e_name="Alice Smith",
        e_pos="Software Engineer",
        e_sal=80000,
    ),
    Employee(
        e_id=2,
        e_name="Bob Johnson",
        e_pos="Data Scientist",
        e_sal=90000,
    ),
    Employee(
        e_id=3,
        e_name="Carol Williams",
        e_pos="Product Manager",
        e_sal=95000,
    ),
    Employee(
        e_id=4,
        e_name="David Brown",
        e_pos="UX Designer",
        e_sal=70000,
    ),
    Employee(
        e_id=5,
        e_name="Eve Davis",
        e_pos="DevOps Engineer",
        e_sal=85000,
    ),
]
