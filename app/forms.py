""" Module defining form schemas """

# Imports
import inspect
from typing import Optional, Type
from fastapi import Form
from pydantic import EmailStr, BaseModel
# from fastapi import FastAPI, Form

from app.schemas import ORMBase

# Look it up

# def form_body(cls: Type[BaseModel]):
#     """
#     Adds an as_form class method to decorated models. The as_form class method
#     can be used with FastAPI endpoints
#     """
#     new_params = [
#         inspect.Parameter(
#             field.alias,
#             inspect.Parameter.POSITIONAL_ONLY,
#             # default=(Form(field.default) if not field.required else Form(...)),
#             # default=(Form(field.default))
#         )
#         for field in cls.model_fields.values()
#     ]


#     def _as_form(**data):
#         return cls(**data)

#     sig = inspect.signature(_as_form)
#     sig = sig.replace(parameters=new_params)
#     _as_form.__signature__ = sig
#     setattr(cls, "as_form", _as_form)
#     return cls

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class PostCreate(ORMBase):
    description: Optional[str] = None
    published: Optional[bool] = True
    location: Optional[str]
    deleted: Optional[bool] = False