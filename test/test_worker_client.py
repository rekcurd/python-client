import time
import unittest

import grpc
from grpc.framework.foundation import logging_pool
import grpc_testing

from rekcurd_client.protobuf import rekcurd_pb2
from . import _client_application


target_service = rekcurd_pb2.DESCRIPTOR.services_by_name['RekcurdWorker']


class RekcurdWorkerClientTest(unittest.TestCase):

    def setUp(self):
        self._client_execution_thread_pool = logging_pool.pool(1)
        self._fake_time = grpc_testing.strict_fake_time(time.time())
        self._real_time = grpc_testing.strict_real_time()
        self._fake_time_channel = grpc_testing.channel(
            rekcurd_pb2.DESCRIPTOR.services_by_name.values(), self._fake_time)
        self._real_time_channel = grpc_testing.channel(
            rekcurd_pb2.DESCRIPTOR.services_by_name.values(), self._real_time)

    def tearDown(self):
        self._client_execution_thread_pool.shutdown(wait=True)

    def test_metadata(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_STRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_String_String']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(invocation_metadata[0], ('x-rekcurd-application-name', 'rekcurd-sample'))
        self.assertEqual(invocation_metadata[1], ('x-rekcurd-sevice-level', 'development'))

    def test_String_String(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_STRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_String_String']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_String_Bytes(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_BYTES,
            self._fake_time_channel)
        invocation_metadata, request, rpc = (
            self._fake_time_channel.take_unary_stream(
                target_service.methods_by_name['Predict_String_Bytes']))
        rpc.send_initial_metadata(())
        rpc.terminate((), grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_String_ArrInt(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_ARRINT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_String_ArrInt']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_INT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_String_ArrFloat(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_ARRFLOAT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_String_ArrFloat']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_FLOAT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_String_ArrString(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.STRING_ARRSTRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_String_ArrString']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_Bytes_String(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.BYTES_STRING,
            self._real_time_channel)
        invocation_metadata, rpc = self._real_time_channel.take_stream_unary(
            target_service.methods_by_name['Predict_Bytes_String'])
        rpc.send_initial_metadata(())
        first_request = rpc.take_request()
        second_request = rpc.take_request()
        third_request = rpc.take_request()
        rpc.requests_closed()
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, first_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, second_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, third_request)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_Bytes_Bytes(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.BYTES_BYTES,
            self._fake_time_channel)
        invocation_metadata, rpc = self._fake_time_channel.take_stream_stream(
            target_service.methods_by_name['Predict_Bytes_Bytes'])
        first_request = rpc.take_request()
        rpc.send_response(_client_application.Response.BYTES_RESPONSE.value)
        rpc.send_response(_client_application.Response.BYTES_RESPONSE.value)
        second_request = rpc.take_request()
        rpc.send_response(_client_application.Response.BYTES_RESPONSE.value)
        rpc.send_response(_client_application.Response.BYTES_RESPONSE.value)
        rpc.requests_closed()
        rpc.terminate((), grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.BYTES_REQUEST.value,
                         first_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value,
                         second_request)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_Bytes_ArrInt(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.BYTES_ARRINT,
            self._real_time_channel)
        invocation_metadata, rpc = self._real_time_channel.take_stream_unary(
            target_service.methods_by_name['Predict_Bytes_ArrInt'])
        rpc.send_initial_metadata(())
        first_request = rpc.take_request()
        second_request = rpc.take_request()
        third_request = rpc.take_request()
        rpc.requests_closed()
        rpc.terminate(_client_application.Response.ARRAY_INT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, first_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, second_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, third_request)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_Bytes_ArrFloat(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.BYTES_ARRFLOAT,
            self._real_time_channel)
        invocation_metadata, rpc = self._real_time_channel.take_stream_unary(
            target_service.methods_by_name['Predict_Bytes_ArrFloat'])
        rpc.send_initial_metadata(())
        first_request = rpc.take_request()
        second_request = rpc.take_request()
        third_request = rpc.take_request()
        rpc.requests_closed()
        rpc.terminate(_client_application.Response.ARRAY_FLOAT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, first_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, second_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, third_request)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_Bytes_ArrString(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.BYTES_ARRSTRING,
            self._real_time_channel)
        invocation_metadata, rpc = self._real_time_channel.take_stream_unary(
            target_service.methods_by_name['Predict_Bytes_ArrString'])
        rpc.send_initial_metadata(())
        first_request = rpc.take_request()
        second_request = rpc.take_request()
        third_request = rpc.take_request()
        rpc.requests_closed()
        rpc.terminate(_client_application.Response.ARRAY_STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, first_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, second_request)
        self.assertEqual(_client_application.Request.BYTES_REQUEST.value, third_request)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrInt_String(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRINT_STRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrInt_String']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_INT_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrInt_Bytes(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRINT_BYTES,
            self._fake_time_channel)
        invocation_metadata, request, rpc = (
            self._fake_time_channel.take_unary_stream(
                target_service.methods_by_name['Predict_ArrInt_Bytes']))
        rpc.send_initial_metadata(())
        rpc.terminate((), grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_INT_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrInt_ArrInt(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRINT_ARRINT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrInt_ArrInt']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_INT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_INT_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrInt_ArrFloat(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRINT_ARRFLOAT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrInt_ArrFloat']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_FLOAT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_INT_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrInt_ArrString(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRINT_ARRSTRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrInt_ArrString']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_INT_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrFloat_String(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRFLOAT_STRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrFloat_String']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertAlmostEqual(_client_application.Request.ARRAY_FLOAT_REQUEST.value[0], request.input[0])
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrFloat_Bytes(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRFLOAT_BYTES,
            self._fake_time_channel)
        invocation_metadata, request, rpc = (
            self._fake_time_channel.take_unary_stream(
                target_service.methods_by_name['Predict_ArrFloat_Bytes']))
        rpc.send_initial_metadata(())
        rpc.terminate((), grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertAlmostEqual(_client_application.Request.ARRAY_FLOAT_REQUEST.value[0], request.input[0])
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrFloat_ArrInt(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRFLOAT_ARRINT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrFloat_ArrInt']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_INT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertAlmostEqual(_client_application.Request.ARRAY_FLOAT_REQUEST.value[0], request.input[0])
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrFloat_ArrFloat(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRFLOAT_ARRFLOAT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrFloat_ArrFloat']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_FLOAT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertAlmostEqual(_client_application.Request.ARRAY_FLOAT_REQUEST.value[0], request.input[0])
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrFloat_ArrString(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRFLOAT_ARRSTRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrFloat_ArrString']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertAlmostEqual(_client_application.Request.ARRAY_FLOAT_REQUEST.value[0], request.input[0])
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrString_String(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRSTRING_STRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrString_String']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrString_Bytes(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRSTRING_BYTES,
            self._fake_time_channel)
        invocation_metadata, request, rpc = (
            self._fake_time_channel.take_unary_stream(
                target_service.methods_by_name['Predict_ArrString_Bytes']))
        rpc.send_initial_metadata(())
        rpc.terminate((), grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrString_ArrInt(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRSTRING_ARRINT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrString_ArrInt']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_INT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrString_ArrFloat(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRSTRING_ARRFLOAT,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrString_ArrFloat']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_FLOAT_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)

    def test_ArrString_ArrString(self):
        application_future = self._client_execution_thread_pool.submit(
            _client_application.run, _client_application.Scenario.ARRSTRING_ARRSTRING,
            self._real_time_channel)
        invocation_metadata, request, rpc = (
            self._real_time_channel.take_unary_unary(
                target_service.methods_by_name['Predict_ArrString_ArrString']))
        rpc.send_initial_metadata(())
        rpc.terminate(_client_application.Response.ARRAY_STRING_RESPONSE.value, (),
                      grpc.StatusCode.OK, '')
        application_return_value = application_future.result()

        self.assertEqual(_client_application.Request.ARRAY_STRING_REQUEST.value, request.input)
        self.assertIs(application_return_value.kind,
                      _client_application.Outcome.Kind.SATISFACTORY)
