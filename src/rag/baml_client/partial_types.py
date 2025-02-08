###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, Generic, List, Optional, TypeVar, Union, Literal

from . import types
from .types import Checked, Check

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################

T = TypeVar('T')
class StreamState(BaseModel, Generic[T]):
    value: T
    state: Literal["Pending", "Incomplete", "Complete"]


class Answer(BaseModel):
    title: Optional[Union[Optional[str], Optional[None]]] = None
    question: Optional[str] = None
    answer: Optional[Union[Optional[str], Optional[None]]] = None

class Context(BaseModel):
    documents: List["Document"]

class Document(BaseModel):
    title: Optional[Union[Optional[str], Optional[None]]] = None
    year: Optional[Union[Optional[int], Optional[None]]] = None
    summary: Optional[Union[Optional[str], Optional[None]]] = None
    plot: Optional[Union[Optional[str], Optional[None]]] = None
    distance: Optional[float] = None
