###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401,F821
# flake8: noqa: E501,F401,F821
# pylint: disable=unused-import,line-too-long
# fmt: off
from typing import Any, Dict, List, Optional, TypeVar, Union, TypedDict, Type, Literal, cast
from typing_extensions import NotRequired
import pprint

import baml_py
from pydantic import BaseModel, ValidationError, create_model

from . import partial_types, types
from .types import Checked, Check
from .type_builder import TypeBuilder
from .globals import DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX, DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME
from .sync_request import HttpRequest, HttpStreamRequest
from .parser import LlmResponseParser, LlmStreamParser

OutputType = TypeVar('OutputType')


# Define the TypedDict with optional parameters having default values
class BamlCallOptions(TypedDict, total=False):
    tb: NotRequired[TypeBuilder]
    client_registry: NotRequired[baml_py.baml_py.ClientRegistry]
    collector: NotRequired[Union[baml_py.baml_py.Collector, List[baml_py.baml_py.Collector]]]


class BamlSyncClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager
    __stream_client: "BamlStreamClient"
    __http_request: "HttpRequest"
    __http_stream_request: "HttpStreamRequest"
    __llm_response_parser: LlmResponseParser
    __baml_options: BamlCallOptions

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager, baml_options: Optional[BamlCallOptions] = None):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager
      self.__stream_client = BamlStreamClient(self.__runtime, self.__ctx_manager, baml_options)
      self.__http_request = HttpRequest(self.__runtime, self.__ctx_manager)
      self.__http_stream_request = HttpStreamRequest(self.__runtime, self.__ctx_manager)
      self.__llm_response_parser = LlmResponseParser(self.__runtime, self.__ctx_manager)
      self.__llm_stream_parser = LlmStreamParser(self.__runtime, self.__ctx_manager)
      self.__baml_options = baml_options or {}

    @property
    def stream(self):
      return self.__stream_client

    @property
    def request(self):
      return self.__http_request

    @property
    def stream_request(self):
      return self.__http_stream_request

    @property
    def parse(self):
      return self.__llm_response_parser

    @property
    def parse_stream(self):
      return self.__llm_stream_parser

    def with_options(
      self,
      tb: Optional[TypeBuilder] = None,
      client_registry: Optional[baml_py.baml_py.ClientRegistry] = None,
      collector: Optional[Union[baml_py.baml_py.Collector, List[baml_py.baml_py.Collector]]] = None,
    ) -> "BamlSyncClient":
      """
      Returns a new instance of BamlSyncClient with explicitly typed baml options
      for Python 3.8 compatibility.
      """
      new_options: BamlCallOptions = self.__baml_options.copy()

      # Override if any keyword arguments were provided.
      if tb is not None:
          new_options["tb"] = tb
      if client_registry is not None:
          new_options["client_registry"] = client_registry
      if collector is not None:
          new_options["collector"] = collector
      return BamlSyncClient(self.__runtime, self.__ctx_manager, new_options)

    
    def ClassifyGender(
        self,
        info: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Gender:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "ClassifyGender",
        {
          "info": info,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Gender, raw.cast_to(types, types, partial_types, False))
    
    def ClassifyGenderCoD(
        self,
        info: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Gender:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "ClassifyGenderCoD",
        {
          "info": info,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Gender, raw.cast_to(types, types, partial_types, False))
    



class BamlStreamClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager
    __baml_options: BamlCallOptions
    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager, baml_options: Optional[BamlCallOptions] = None):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager
      self.__baml_options = baml_options or {}

    
    def ClassifyGender(
        self,
        info: str,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[Optional[types.Gender], types.Gender]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "ClassifyGender",
        {
          "info": info,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[Optional[types.Gender], types.Gender](
        raw,
        lambda x: cast(Optional[types.Gender], x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Gender, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    
    def ClassifyGenderCoD(
        self,
        info: str,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[Optional[types.Gender], types.Gender]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "ClassifyGenderCoD",
        {
          "info": info,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[Optional[types.Gender], types.Gender](
        raw,
        lambda x: cast(Optional[types.Gender], x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Gender, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    


b = BamlSyncClient(DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME, DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX)

__all__ = ["b"]