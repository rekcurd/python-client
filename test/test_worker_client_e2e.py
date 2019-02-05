import grpc
from concurrent import futures

from . import *
from rekcurd_client.protobuf import rekcurd_pb2_grpc
import unittest
from functools import wraps
from unittest.mock import patch, Mock

from rekcurd.utils import PredictResult
import rekcurd_client.rekcurd_worker_client


def patch_predictor(input_type, output_type):
    """Decorator to mock the predictor.
    Patch the several methods of the Predict class to make a fake predictor.
    """

    _prediction_value_map = {
        Type.STRING: PredictResult('Rekcurd', 1.0, option={}),
        Type.BYTES: PredictResult(b'\x8f\xfa;\xc8a\xa3T%', 1.0, option={}),
        Type.ARRAY_INT: PredictResult([2, 3, 5, 7], [1.0, 1.0, 1.0, 1.0], option={}),
        Type.ARRAY_FLOAT: PredictResult([0.78341155, 0.03166816, 0.92745938], [1.0, 1.0, 1.0], option={}),
        Type.ARRAY_STRING: PredictResult(['Rekcurd', 'is', 'awesome'], [1.0, 1.0, 1.0], option={}),
    }

    def test_method(func):
        @wraps(func)
        def inner_method(*args, **kwargs):
            with patch('test.dummy_app.DummyApp.get_type_input',
                       new=Mock(return_value=input_type)) as _, \
                    patch('test.dummy_app.DummyApp.get_type_output',
                          new=Mock(return_value=output_type)) as _, \
                    patch('test.dummy_app.DummyApp.load_model') as _, \
                    patch('test.dummy_app.DummyApp.predict',
                          new=Mock(return_value=_prediction_value_map[output_type])) as _:
                return func(*args, **kwargs)
        return inner_method
    return test_method


class RekcurdWorkerClientTestE2E(unittest.TestCase):
    """Tests for RekcurdWorkerClient. This test is e2e test between rekcurd-python and python-client."""

    def fake_string_input(self):
        return 'Rekcurd'

    def fake_bytes_input(self):
        return b'u\x95jD\x0c\xf4\xf4{\xa6\xd7'

    def fake_arrint_input(self):
        return [124, 117,   2, 216]

    def fake_arrfloat_input(self):
        return [0.51558887, 0.07656534, 0.64258131, 0.45239403, 0.53738411,
                0.3863864, 0.33985784]

    def fake_arrstring_input(self):
        return ['Rekcurd', 'is', 'great']

    def assertStringResponse(self, response):
        self.assertEqual(response.__class__.__name__, "StringOutput")

    def assertBytesResponse(self, response):
        for item in response:
            self.assertEqual(item.__class__.__name__, "BytesOutput")

    def assertArrIntResponse(self, response):
        self.assertEqual(response.__class__.__name__, "ArrIntOutput")

    def assertArrFloatResponse(self, response):
        self.assertEqual(response.__class__.__name__, "ArrFloatOutput")

    def assertArrStringResponse(self, response):
        self.assertEqual(response.__class__.__name__, "ArrStringOutput")

    server = None
    client = None

    @classmethod
    def setUpClass(cls):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        rekcurd_pb2_grpc.add_RekcurdWorkerServicer_to_server(
            rekcurd.rekcurd_worker_servicer.RekcurdWorkerServicer(
                logger=service_logger, app=app),
            server)
        server.add_insecure_port("[::]:5000")
        server.start()
        cls.server = server
        cls.client = rekcurd_client.rekcurd_worker_client.RekcurdWorkerClient(logger=client_logger, host='127.0.0.1:5000')

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'server'):
            cls.server.stop(0)

    @patch_predictor(Type.STRING, Type.STRING)
    def test_string_string(self):
        response = self.client.run_predict_string_string(self.fake_string_input())
        self.assertStringResponse(response)

    @patch_predictor(Type.STRING, Type.BYTES)
    def test_string_bytes(self):
        response = self.client.run_predict_string_bytes(self.fake_string_input())
        self.assertBytesResponse(response)

    @patch_predictor(Type.STRING, Type.ARRAY_INT)
    def test_string_arrint(self):
        response = self.client.run_predict_string_arrint(self.fake_string_input())
        self.assertArrIntResponse(response)

    @patch_predictor(Type.STRING, Type.ARRAY_FLOAT)
    def test_string_arrfloat(self):
        response = self.client.run_predict_string_arrfloat(self.fake_string_input())
        self.assertArrFloatResponse(response)

    @patch_predictor(Type.STRING, Type.ARRAY_STRING)
    def test_string_arrstring(self):
        response = self.client.run_predict_string_arrstring(self.fake_string_input())
        self.assertArrStringResponse(response)

    @patch_predictor(Type.BYTES, Type.STRING)
    def test_bytes_string(self):
        response = self.client.run_predict_bytes_string(self.fake_bytes_input())
        self.assertStringResponse(response)

    @patch_predictor(Type.BYTES, Type.BYTES)
    def test_bytes_bytes(self):
        response = self.client.run_predict_bytes_bytes(self.fake_bytes_input())
        self.assertBytesResponse(response)

    @patch_predictor(Type.BYTES, Type.ARRAY_INT)
    def test_bytes_arrint(self):
        response = self.client.run_predict_bytes_arrint(self.fake_bytes_input())
        self.assertArrIntResponse(response)

    @patch_predictor(Type.BYTES, Type.ARRAY_FLOAT)
    def test_bytes_arrfloat(self):
        response = self.client.run_predict_bytes_arrfloat(self.fake_bytes_input())
        self.assertArrFloatResponse(response)

    @patch_predictor(Type.BYTES, Type.ARRAY_STRING)
    def test_bytes_arrstring(self):
        response = self.client.run_predict_bytes_arrstring(self.fake_bytes_input())
        self.assertArrStringResponse(response)

    @patch_predictor(Type.ARRAY_INT, Type.STRING)
    def test_arrint_string(self):
        response = self.client.run_predict_arrint_string(self.fake_arrint_input())
        self.assertStringResponse(response)

    @patch_predictor(Type.ARRAY_INT, Type.BYTES)
    def test_arrint_bytes(self):
        response = self.client.run_predict_arrint_bytes(self.fake_arrint_input())
        self.assertBytesResponse(response)

    @patch_predictor(Type.ARRAY_INT, Type.ARRAY_INT)
    def test_arrint_arrint(self):
        response = self.client.run_predict_arrint_arrint(self.fake_arrint_input())
        self.assertArrIntResponse(response)

    @patch_predictor(Type.ARRAY_INT, Type.ARRAY_FLOAT)
    def test_arrint_arrfloat(self):
        response = self.client.run_predict_arrint_arrfloat(self.fake_arrint_input())
        self.assertArrFloatResponse(response)

    @patch_predictor(Type.ARRAY_INT, Type.ARRAY_STRING)
    def test_arrint_arrstring(self):
        response = self.client.run_predict_arrint_arrstring(self.fake_arrint_input())
        self.assertArrStringResponse(response)

    @patch_predictor(Type.ARRAY_FLOAT, Type.STRING)
    def test_arrfloat_string(self):
        response = self.client.run_predict_arrfloat_string(self.fake_arrfloat_input())
        self.assertStringResponse(response)

    @patch_predictor(Type.ARRAY_FLOAT, Type.BYTES)
    def test_arrfloat_bytes(self):
        response = self.client.run_predict_arrfloat_bytes(self.fake_arrfloat_input())
        self.assertBytesResponse(response)

    @patch_predictor(Type.ARRAY_FLOAT, Type.ARRAY_INT)
    def test_arrfloat_arrint(self):
        response = self.client.run_predict_arrfloat_arrint(self.fake_arrfloat_input())
        self.assertArrIntResponse(response)

    @patch_predictor(Type.ARRAY_FLOAT, Type.ARRAY_FLOAT)
    def test_arrfloat_arrfloat(self):
        response = self.client.run_predict_arrfloat_arrfloat(self.fake_arrfloat_input())
        self.assertArrFloatResponse(response)

    @patch_predictor(Type.ARRAY_FLOAT, Type.ARRAY_STRING)
    def test_arrfloat_arrstring(self):
        response = self.client.run_predict_arrfloat_arrstring(self.fake_arrfloat_input())
        self.assertArrStringResponse(response)

    @patch_predictor(Type.ARRAY_STRING, Type.STRING)
    def test_arrstring_string(self):
        response = self.client.run_predict_arrstring_string(self.fake_arrstring_input())
        self.assertStringResponse(response)

    @patch_predictor(Type.ARRAY_STRING, Type.BYTES)
    def test_arrstring_bytes(self):
        response = self.client.run_predict_arrstring_bytes(self.fake_arrstring_input())
        self.assertBytesResponse(response)

    @patch_predictor(Type.ARRAY_STRING, Type.ARRAY_INT)
    def test_arrstring_arrint(self):
        response = self.client.run_predict_arrstring_arrint(self.fake_arrstring_input())
        self.assertArrIntResponse(response)

    @patch_predictor(Type.ARRAY_STRING, Type.ARRAY_FLOAT)
    def test_arrstring_arrfloat(self):
        response = self.client.run_predict_arrstring_arrfloat(self.fake_arrstring_input())
        self.assertArrFloatResponse(response)

    @patch_predictor(Type.ARRAY_STRING, Type.ARRAY_STRING)
    def test_arrstring_arrstring(self):
        response = self.client.run_predict_arrstring_arrstring(self.fake_arrstring_input())
        self.assertArrStringResponse(response)
