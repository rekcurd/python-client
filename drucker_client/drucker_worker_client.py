#!/usr/bin/python
# -*- coding: utf-8 -*-


import traceback
import types
import grpc

from .protobuf import drucker_pb2, drucker_pb2_grpc
from .logger import SystemLoggerInterface


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
    def __init__(self, logger: SystemLoggerInterface,
                 host: str = None,
                 domain: str = None, app: str = None,
                 env: str = None, version: int = None):
        self.logger = logger
        self.stub = None
        if host is None and (domain is None or app is None or env is None):
            raise RuntimeError("You must specify url or domain+app+env.")

        if version is None:
            v_str = drucker_pb2.DESCRIPTOR.GetOptions().Extensions[drucker_pb2.drucker_grpc_proto_version]
        else:
            v_str = drucker_pb2.EnumVersionInfo.Name(version)

        self.__metadata = [('x-rekcurd-application-name', app),
                           ('x-rekcurd-sevice-level', env),
                           ('x-rekcurd-grpc-version', v_str)]
        if host is None:
            self.__change_domain_app_env(domain, app, env, v_str)
        else:
            self.__change_host(host)

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

    def __change_domain_app_env(self, domain: str, app: str, env: str, version: str):
        host = "{0}-{1}-{2}.{3}".format(app,version,env,domain)
        self.__change_host(host)

    def __change_host(self, host: str):
        channel = grpc.insecure_channel(host)
        self.stub = drucker_pb2_grpc.DruckerWorkerStub(channel)

    def __byte_input_request(self, input, option="{}"):
        yield drucker_pb2.BytesInput(input=input, option=drucker_pb2.Option(val=option))


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_string_string(self, input, option="{}"):
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=option
        response = self.stub.Predict_String_String(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_string_bytes(self, input, option="{}"):
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=option
        response = self.stub.Predict_String_Bytes(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_string_arrint(self, input, option="{}"):
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=option
        response = self.stub.Predict_String_ArrInt(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_string_arrfloat(self, input, option="{}"):
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=option
        response = self.stub.Predict_String_ArrFloat(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_string_arrstring(self, input, option="{}"):
        request = drucker_pb2.StringInput()
        request.input = input
        request.option.val=option
        response = self.stub.Predict_String_ArrString(request, metadata=self.__metadata)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_bytes_string(self, input, option="{}"):
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_String(request_iterator, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_bytes_bytes(self, input, option="{}"):
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_Bytes(request_iterator, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_bytes_arrint(self, input, option="{}"):
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrInt(request_iterator, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_bytes_arrfloat(self, input, option="{}"):
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrFloat(request_iterator, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_bytes_arrstring(self, input, option="{}"):
        request_iterator = self.__byte_input_request(input, option)
        response = self.stub.Predict_Bytes_ArrString(request_iterator, metadata=self.__metadata)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrint_string(self, input, option="{}"):
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrInt_String(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrint_bytes(self, input, option="{}"):
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrInt_Bytes(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrint_arrint(self, input, option="{}"):
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrInt_ArrInt(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrint_arrfloat(self, input, option="{}"):
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrInt_ArrFloat(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrint_arrstring(self, input, option="{}"):
        request = drucker_pb2.ArrIntInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrInt_ArrString(request, metadata=self.__metadata)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrfloat_string(self, input, option="{}"):
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrFloat_String(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrfloat_bytes(self, input, option="{}"):
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrFloat_Bytes(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrfloat_arrint(self, input, option="{}"):
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrFloat_ArrInt(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrfloat_arrfloat(self, input, option="{}"):
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrFloat_ArrFloat(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrfloat_arrstring(self, input, option="{}"):
        request = drucker_pb2.ArrFloatInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrFloat_ArrString(request, metadata=self.__metadata)
        return response


    @error_handling(drucker_pb2.StringOutput())
    def run_predict_arrstring_string(self, input, option="{}"):
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrString_String(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.BytesOutput())
    def run_predict_arrstring_bytes(self, input, option="{}"):
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrString_Bytes(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrIntOutput())
    def run_predict_arrstring_arrint(self, input, option="{}"):
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrString_ArrInt(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrFloatOutput())
    def run_predict_arrstring_arrfloat(self, input, option="{}"):
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrString_ArrFloat(request, metadata=self.__metadata)
        return response

    @error_handling(drucker_pb2.ArrStringOutput())
    def run_predict_arrstring_arrstring(self, input, option="{}"):
        request = drucker_pb2.ArrStringInput()
        request.input.extend(input)
        request.option.val=option
        response = self.stub.Predict_ArrString_ArrString(request, metadata=self.__metadata)
        return response
