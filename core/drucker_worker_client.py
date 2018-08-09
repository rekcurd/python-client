#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# DO NOT EDIT HERE!!

import traceback
import types
import grpc
import json

import drucker_pb2
import drucker_pb2_grpc

from typing import Union, List

from logger.logger_interface import SystemLoggerInterface


DruckerInputType = Union[int, float, bool, str, bytes,
                         List[Union[int, float, bool, str]]]
DruckerOutputType = Union[int, float, bool, str, bytes,
                          List[Union[int, float, bool, str]]]
DruckerScoreType = Union[float, List[float]]


dict_any_type_url = {
    'type.googleapis.com/%s'%drucker_pb2.SingleInt32().DESCRIPTOR.full_name: (drucker_pb2.SingleInt32(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleInt64().DESCRIPTOR.full_name: (drucker_pb2.SingleInt64(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleUint32().DESCRIPTOR.full_name: (drucker_pb2.SingleUint32(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleUint64().DESCRIPTOR.full_name: (drucker_pb2.SingleUint64(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleSint32().DESCRIPTOR.full_name: (drucker_pb2.SingleSint32(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleSint64().DESCRIPTOR.full_name: (drucker_pb2.SingleSint64(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleFixed32().DESCRIPTOR.full_name: (drucker_pb2.SingleFixed32(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleFixed64().DESCRIPTOR.full_name: (drucker_pb2.SingleFixed64(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleSfixed32().DESCRIPTOR.full_name: (drucker_pb2.SingleSfixed32(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleSfixed64().DESCRIPTOR.full_name: (drucker_pb2.SingleSfixed64(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleFloat().DESCRIPTOR.full_name: (drucker_pb2.SingleFloat(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleDouble().DESCRIPTOR.full_name: (drucker_pb2.SingleDouble(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleBool().DESCRIPTOR.full_name: (drucker_pb2.SingleBool(), True),
    'type.googleapis.com/%s'%drucker_pb2.SingleString().DESCRIPTOR.full_name: (drucker_pb2.SingleString(), True),
    'type.googleapis.com/%s'%drucker_pb2.ArrInt32().DESCRIPTOR.full_name: (drucker_pb2.ArrInt32(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrInt64().DESCRIPTOR.full_name: (drucker_pb2.ArrInt64(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrUint32().DESCRIPTOR.full_name: (drucker_pb2.ArrUint32(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrUint64().DESCRIPTOR.full_name: (drucker_pb2.ArrUint64(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrSint32().DESCRIPTOR.full_name: (drucker_pb2.ArrSint32(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrSint64().DESCRIPTOR.full_name: (drucker_pb2.ArrSint64(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrFixed32().DESCRIPTOR.full_name: (drucker_pb2.ArrFixed32(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrFixed64().DESCRIPTOR.full_name: (drucker_pb2.ArrFixed64(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrSfixed32().DESCRIPTOR.full_name: (drucker_pb2.ArrSfixed32(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrSfixed64().DESCRIPTOR.full_name: (drucker_pb2.ArrSfixed64(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrFloat().DESCRIPTOR.full_name: (drucker_pb2.ArrFloat(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrDouble().DESCRIPTOR.full_name: (drucker_pb2.ArrDouble(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrBool().DESCRIPTOR.full_name: (drucker_pb2.ArrBool(), False),
    'type.googleapis.com/%s'%drucker_pb2.ArrString().DESCRIPTOR.full_name: (drucker_pb2.ArrString(), False),
}

class DruckerOutput:
    output=None
    score=None
    option=None
    def __init__(self,
                 output:DruckerOutputType=None,
                 score:DruckerScoreType=None,
                 option:dict=None):
        self.output=output
        self.score=score
        self.option=option
    def __str__(self):
        return str({
            "output": self.output,
            "score": self.score,
            "option": self.option
        })


def error_handling(error_response):
    """ Decorator for handling error

    Apply following processing on Servicer methods
    to handle errors.

    - Call :func:``on_error`` method (if defined) in the class
      to postprocess something on error

    Parameters
    ----------
    error_response
    """
    def _wrapper_maker(func):
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                servicer = args[0]
                if hasattr(servicer, 'on_error'):
                    assert isinstance(servicer.on_error, types.MethodType), \
                        'You must define on_error as method'
                    servicer.on_error(error)
                return error_response
        return _wrapper
    return _wrapper_maker


class DruckerWorkerClient:
    def __init__(self, logger:SystemLoggerInterface,
                 input_type:type=None, output_type:type=None,
                 host:str=None,
                 domain:str=None, app:str=None, env:str=None, version:int=None):
        self.logger = logger
        self.stub = None

        if host is None and (domain is None or app is None or env is None):
            raise RuntimeError("You must specify url or domain+app+env.")

        if version is None:
            v_str = drucker_pb2.DESCRIPTOR.GetOptions().Extensions[drucker_pb2.drucker_grpc_proto_version]
        else:
            v_str = drucker_pb2.EnumVersionInfo.Name(version)

        if host is None:
            self.__change_domain_app_env(domain, app, env, v_str)
        else:
            self.__change_host(host)

        if input_type is bytes:
            if output_type is bytes:
                self.executor = self.stub.Predict_File_File
            else:
                self.executor = self.stub.Predict_File_Any
        else:
            if output_type is bytes:
                self.executor = self.stub.Predict_Any_File
            else:
                self.executor = self.stub.Predict_Any_Any

    def on_error(self, error: Exception):
        """ Postprocessing on error

        For detail, see :func:``on_error``

        Parameters
        ----------
        error : Exception
            Error to be handled
        """
        self.logger.error(str(error))
        self.logger.error(traceback.format_exc())

    def __change_domain_app_env(self, domain:str, app:str, env:str, version:str):
        host = "{0}-{1}-{2}.{3}".format(app,version,env,domain)
        self.__change_host(host)

    def __change_host(self, host:str):
        channel = grpc.insecure_channel(host)
        self.stub = drucker_pb2_grpc.DruckerWorkerStub(channel)

    def __byte_input_request(self, input:bytes, option:dict):
        yield drucker_pb2.BytesInput(
            input=input,
            option=drucker_pb2.Option(val=json.dumps(option)))

    @error_handling(DruckerOutput())
    def predict(self, input:DruckerInputType, option:dict={}) -> DruckerOutput:
        if isinstance(input, bytes):
            request_iterator = self.__byte_input_request(input, option)
            response = self.executor(request_iterator)
        else:
            if isinstance(input, list):
                chk = input[0]
                if isinstance(chk, int):
                    ival = drucker_pb2.ArrInt64()
                elif isinstance(chk, float):
                    ival = drucker_pb2.ArrFloat()
                elif isinstance(chk, bool):
                    ival = drucker_pb2.ArrBool()
                elif isinstance(chk, str):
                    ival = drucker_pb2.ArrString()
                else:
                    ival = None
                ival.val.extend(input)
            else:
                chk = input
                if isinstance(chk, int):
                    ival = drucker_pb2.SingleInt64()
                elif isinstance(chk, float):
                    ival = drucker_pb2.SingleFloat()
                elif isinstance(chk, bool):
                    ival = drucker_pb2.SingleBool()
                elif isinstance(chk, str):
                    ival = drucker_pb2.SingleString()
                else:
                    ival = None
                ival.val = input
            request = drucker_pb2.AnyInput()
            request.input.Pack(ival)
            request.option.val=json.dumps(option)
            response = self.executor(request)
        output = DruckerOutput()
        if isinstance(response, drucker_pb2.AnyOutput):
            output_message, is_single = \
                dict_any_type_url.get(response.output.type_url, None)
            response.output.Unpack(output_message)
            output.output = output_message.val
            if is_single:
                output.score = response.score[0]
            else:
                output.score = response.score
            output.option = json.loads(response.option.val)
        else:
            output.output = response.output
            output.score = response.score
            output.option = json.loads(response.option.val)
        return output

    @error_handling(drucker_pb2.StringOutput())
    def run_predict_string_string(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=json.dumps(option)
        response = self.stub.Predict_String_String(request)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_string_bytes(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=json.dumps(option)
        response = self.stub.Predict_String_Bytes(request)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_string_arrint(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=json.dumps(option)
        response = self.stub.Predict_String_ArrInt(request)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_string_arrfloat(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=json.dumps(option)
        response = self.stub.Predict_String_ArrFloat(request)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_string_arrstring(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=json.dumps(option)
        response = self.stub.Predict_String_ArrString(request)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_bytes_string(self, input, option:dict={}):
        """@deprecated
        """
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_String(request_iterator)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_bytes_bytes(self, input, option:dict={}):
        """@deprecated
        """
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_Bytes(request_iterator)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_bytes_arrint(self, input, option:dict={}):
        """@deprecated
        """
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrInt(request_iterator)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_bytes_arrfloat(self, input, option:dict={}):
        """@deprecated
        """
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrFloat(request_iterator)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_bytes_arrstring(self, input, option:dict={}):
        """@deprecated
        """
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrString(request_iterator)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrint_string(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrInt_String(request)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrint_bytes(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrInt_Bytes(request)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrint_arrint(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrInt_ArrInt(request)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrint_arrfloat(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrInt_ArrFloat(request)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrint_arrstring(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrInt_ArrString(request)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrfloat_string(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrFloat_String(request)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrfloat_bytes(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrFloat_Bytes(request)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrfloat_arrint(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrFloat_ArrInt(request)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrfloat_arrfloat(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrFloat_ArrFloat(request)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrfloat_arrstring(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrFloat_ArrString(request)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrstring_string(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrString_String(request)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrstring_bytes(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrString_Bytes(request)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrstring_arrint(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrString_ArrInt(request)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrstring_arrfloat(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrString_ArrFloat(request)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrstring_arrstring(self, input, option:dict={}):
        """@deprecated
        """
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=json.dumps(option)
        response = self.stub.Predict_ArrString_ArrString(request)
        return response
