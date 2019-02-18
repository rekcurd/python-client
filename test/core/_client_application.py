import collections
import enum
import threading
import grpc

from rekcurd.utils import PredictResult

from rekcurd_client.protobuf import rekcurd_pb2_grpc
from rekcurd_client import RekcurdWorkerClient


@enum.unique
class Scenario(enum.Enum):
    STRING_STRING = 'string_string'
    STRING_BYTES = 'string_bytes'
    STRING_ARRINT = 'string_arrint'
    STRING_ARRFLOAT = 'string_arrfloat'
    STRING_ARRSTRING = 'string_arrstring'
    BYTES_STRING = 'bytes_string'
    BYTES_BYTES = 'bytes_bytes'
    BYTES_ARRINT = 'bytes_arrint'
    BYTES_ARRFLOAT = 'bytes_arrfloat'
    BYTES_ARRSTRING = 'bytes_arrstring'
    ARRINT_STRING = 'arrint_string'
    ARRINT_BYTES = 'arrint_bytes'
    ARRINT_ARRINT = 'arrint_arrint'
    ARRINT_ARRFLOAT = 'arrint_arrfloat'
    ARRINT_ARRSTRING = 'arrint_arrstring'
    ARRFLOAT_STRING = 'arrfloat_string'
    ARRFLOAT_BYTES = 'arrfloat_bytes'
    ARRFLOAT_ARRINT = 'arrfloat_arrint'
    ARRFLOAT_ARRFLOAT = 'arrfloat_arrfloat'
    ARRFLOAT_ARRSTRING = 'arrfloat_arrstring'
    ARRSTRING_STRING = 'arrstring_string'
    ARRSTRING_BYTES = 'arrstring_bytes'
    ARRSTRING_ARRINT = 'arrstring_arrint'
    ARRSTRING_ARRFLOAT = 'arrstring_arrfloat'
    ARRSTRING_ARRSTRING = 'arrstring_arrstring'


class Outcome(collections.namedtuple('Outcome', ('kind', 'code', 'details'))):
    """Outcome of a client application scenario.
    Attributes:
      kind: A Kind value describing the overall kind of scenario execution.
      code: A grpc.StatusCode value. Only valid if kind is Kind.RPC_ERROR.
      details: A status details string. Only valid if kind is Kind.RPC_ERROR.
    """

    @enum.unique
    class Kind(enum.Enum):
        SATISFACTORY = 'satisfactory'
        UNSATISFACTORY = 'unsatisfactory'
        RPC_ERROR = 'rpc error'


_SATISFACTORY_OUTCOME = Outcome(Outcome.Kind.SATISFACTORY, None, None)
_UNSATISFACTORY_OUTCOME = Outcome(Outcome.Kind.UNSATISFACTORY, None, None)


class _Pipe(object):

    def __init__(self):
        self._condition = threading.Condition()
        self._values = []
        self._open = True

    def __iter__(self):
        return self

    def _next(self):
        with self._condition:
            while True:
                if self._values:
                    return self._values.pop(0)
                elif not self._open:
                    raise StopIteration()
                else:
                    self._condition.wait()

    def __next__(self):  # (Python 3 Iterator Protocol)
        return self._next()

    def next(self):  # (Python 2 Iterator Protocol)
        return self._next()

    def add(self, value):
        with self._condition:
            self._values.append(value)
            self._condition.notify_all()

    def close(self):
        with self._condition:
            self._open = False
            self._condition.notify_all()


@enum.unique
class Request(enum.Enum):
    STRING_REQUEST = 'Rekcurd'
    BYTES_REQUEST = b'u\x95jD\x0c\xf4\xf4{\xa6\xd7'
    ARRAY_INT_REQUEST = [124, 117,   2, 216]
    ARRAY_FLOAT_REQUEST = [0.51558887, 0.07656534, 0.64258131, 0.45239403, 0.53738411,
                           0.3863864, 0.33985784]
    ARRAY_STRING_REQUEST = ['Rekcurd', 'is', 'great']


@enum.unique
class Response(enum.Enum):
    STRING_RESPONSE = PredictResult('Rekcurd', 1.0, option={})
    BYTES_RESPONSE = PredictResult(b'\x8f\xfa;\xc8a\xa3T%', 1.0, option={})
    ARRAY_INT_RESPONSE = PredictResult([2, 3, 5, 7], [1.0, 1.0, 1.0, 1.0], option={})
    ARRAY_FLOAT_RESPONSE = PredictResult([0.78341155, 0.03166816, 0.92745938], [1.0, 1.0, 1.0], option={})
    ARRAY_STRING_RESPONSE = PredictResult(['Rekcurd', 'is', 'awesome'], [1.0, 1.0, 1.0], option={})


def _assertStringResponse(response):
    if Response.STRING_RESPONSE.value.label == response.label and \
            Response.STRING_RESPONSE.value.score == response.score and \
            Response.STRING_RESPONSE.value.option == response.option:
        return True
    return False


def _assertBytesResponse(response_iterator):
    try:
        next(response_iterator)
    except StopIteration:
        return True
    else:
        return False


def _assertArrIntResponse(response):
    if Response.ARRAY_INT_RESPONSE.value.label[0] == response.label[0] and \
            Response.ARRAY_INT_RESPONSE.value.score[0] == response.score[0] and \
            Response.ARRAY_INT_RESPONSE.value.option == response.option:
        return True
    return False


def _assertArrFloatResponse(response):
    if Response.ARRAY_FLOAT_RESPONSE.value.label[0] == response.label[0] and \
            Response.ARRAY_FLOAT_RESPONSE.value.score[0] == response.score[0] and \
            Response.ARRAY_FLOAT_RESPONSE.value.option == response.option:
        return True
    return False


def _assertArrStringResponse(response):
    if Response.ARRAY_STRING_RESPONSE.value.label[0] == response.label[0] and \
            Response.ARRAY_STRING_RESPONSE.value.score[0] == response.score[0] and \
            Response.ARRAY_STRING_RESPONSE.value.option == response.option:
        return True
    return False


def _run_string_string(client: RekcurdWorkerClient):
    response = client.run_predict_string_string(Request.STRING_REQUEST.value)
    if _assertStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_string_bytes(client: RekcurdWorkerClient):
    response_iterator = client.run_predict_string_bytes(Request.STRING_REQUEST.value)
    if _assertBytesResponse(response_iterator):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_string_arrint(client: RekcurdWorkerClient):
    response = client.run_predict_string_arrint(Request.STRING_REQUEST.value)
    if _assertArrIntResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_string_arrfloat(client: RekcurdWorkerClient):
    response = client.run_predict_string_arrfloat(Request.STRING_REQUEST.value)
    if _assertArrFloatResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_string_arrstring(client: RekcurdWorkerClient):
    response = client.run_predict_string_arrstring(Request.STRING_REQUEST.value)
    if _assertArrStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_bytes_string(client: RekcurdWorkerClient):
    response, call = client.stub.Predict_Bytes_String.with_call(
        iter((Request.BYTES_REQUEST.value,) * 3))
    if (Response.STRING_RESPONSE.value == response and
        call.code() is grpc.StatusCode.OK):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_bytes_bytes(client: RekcurdWorkerClient):
    request_pipe = _Pipe()
    response_iterator = client.stub.Predict_Bytes_Bytes(iter(request_pipe))
    request_pipe.add(Request.BYTES_REQUEST.value)
    first_responses = next(response_iterator), next(response_iterator),
    request_pipe.add(Request.BYTES_REQUEST.value)
    second_responses = next(response_iterator), next(response_iterator),
    request_pipe.close()
    try:
        next(response_iterator)
    except StopIteration:
        unexpected_extra_response = False
    else:
        unexpected_extra_response = True
    if (first_responses == (Response.BYTES_RESPONSE.value,) * 2 and
            second_responses == (Response.BYTES_RESPONSE.value,) * 2
            and not unexpected_extra_response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_bytes_arrint(client: RekcurdWorkerClient):
    response, call = client.stub.Predict_Bytes_ArrInt.with_call(
        iter((Request.BYTES_REQUEST.value,) * 3))
    if (Response.ARRAY_INT_RESPONSE.value == response and
            call.code() is grpc.StatusCode.OK):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_bytes_arrfloat(client: RekcurdWorkerClient):
    response, call = client.stub.Predict_Bytes_ArrFloat.with_call(
        iter((Request.BYTES_REQUEST.value,) * 3))
    if (Response.ARRAY_FLOAT_RESPONSE.value == response and
            call.code() is grpc.StatusCode.OK):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_bytes_arrstring(client: RekcurdWorkerClient):
    response, call = client.stub.Predict_Bytes_ArrString.with_call(
        iter((Request.BYTES_REQUEST.value,) * 3))
    if (Response.ARRAY_STRING_RESPONSE.value == response and
            call.code() is grpc.StatusCode.OK):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrint_string(client: RekcurdWorkerClient):
    response = client.run_predict_arrint_string(Request.ARRAY_INT_REQUEST.value)
    if _assertStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrint_bytes(client: RekcurdWorkerClient):
    response_iterator = client.run_predict_arrint_bytes(Request.ARRAY_INT_REQUEST.value)
    if _assertBytesResponse(response_iterator):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrint_arrint(client: RekcurdWorkerClient):
    response = client.run_predict_arrint_arrint(Request.ARRAY_INT_REQUEST.value)
    if _assertArrIntResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrint_arrfloat(client: RekcurdWorkerClient):
    response = client.run_predict_arrint_arrfloat(Request.ARRAY_INT_REQUEST.value)
    if _assertArrFloatResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrint_arrstring(client: RekcurdWorkerClient):
    response = client.run_predict_arrint_arrstring(Request.ARRAY_INT_REQUEST.value)
    if _assertArrStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrfloat_string(client: RekcurdWorkerClient):
    response = client.run_predict_arrfloat_string(Request.ARRAY_FLOAT_REQUEST.value)
    if _assertStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrfloat_bytes(client: RekcurdWorkerClient):
    response_iterator = client.run_predict_arrfloat_bytes(Request.ARRAY_FLOAT_REQUEST.value)
    if _assertBytesResponse(response_iterator):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrfloat_arrint(client: RekcurdWorkerClient):
    response = client.run_predict_arrfloat_arrint(Request.ARRAY_FLOAT_REQUEST.value)
    if _assertArrIntResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrfloat_arrfloat(client: RekcurdWorkerClient):
    response = client.run_predict_arrfloat_arrfloat(Request.ARRAY_FLOAT_REQUEST.value)
    if _assertArrFloatResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrfloat_arrstring(client: RekcurdWorkerClient):
    response = client.run_predict_arrfloat_arrstring(Request.ARRAY_FLOAT_REQUEST.value)
    if _assertArrStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrstring_string(client: RekcurdWorkerClient):
    response = client.run_predict_arrstring_string(Request.ARRAY_STRING_REQUEST.value)
    if _assertStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrstring_bytes(client: RekcurdWorkerClient):
    response_iterator = client.run_predict_arrstring_bytes(Request.ARRAY_STRING_REQUEST.value)
    if _assertBytesResponse(response_iterator):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrstring_arrint(client: RekcurdWorkerClient):
    response = client.run_predict_arrstring_arrint(Request.ARRAY_STRING_REQUEST.value)
    if _assertArrIntResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrstring_arrfloat(client: RekcurdWorkerClient):
    response = client.run_predict_arrstring_arrfloat(Request.ARRAY_STRING_REQUEST.value)
    if _assertArrFloatResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_arrstring_arrstring(client: RekcurdWorkerClient):
    response = client.run_predict_arrstring_arrstring(Request.ARRAY_STRING_REQUEST.value)
    if _assertArrStringResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


_IMPLEMENTATIONS = {
    Scenario.STRING_STRING: _run_string_string,
    Scenario.STRING_BYTES: _run_string_bytes,
    Scenario.STRING_ARRINT: _run_string_arrint,
    Scenario.STRING_ARRFLOAT: _run_string_arrfloat,
    Scenario.STRING_ARRSTRING: _run_string_arrstring,
    Scenario.BYTES_STRING: _run_bytes_string,
    Scenario.BYTES_BYTES: _run_bytes_bytes,
    Scenario.BYTES_ARRINT: _run_bytes_arrint,
    Scenario.BYTES_ARRFLOAT: _run_bytes_arrfloat,
    Scenario.BYTES_ARRSTRING: _run_bytes_arrstring,
    Scenario.ARRINT_STRING: _run_arrint_string,
    Scenario.ARRINT_BYTES: _run_arrint_bytes,
    Scenario.ARRINT_ARRINT: _run_arrint_arrint,
    Scenario.ARRINT_ARRFLOAT: _run_arrint_arrfloat,
    Scenario.ARRINT_ARRSTRING: _run_arrint_arrstring,
    Scenario.ARRFLOAT_STRING: _run_arrfloat_string,
    Scenario.ARRFLOAT_BYTES: _run_arrfloat_bytes,
    Scenario.ARRFLOAT_ARRINT: _run_arrfloat_arrint,
    Scenario.ARRFLOAT_ARRFLOAT: _run_arrfloat_arrfloat,
    Scenario.ARRFLOAT_ARRSTRING: _run_arrfloat_arrstring,
    Scenario.ARRSTRING_STRING: _run_arrstring_string,
    Scenario.ARRSTRING_BYTES: _run_arrstring_bytes,
    Scenario.ARRSTRING_ARRINT: _run_arrstring_arrint,
    Scenario.ARRSTRING_ARRFLOAT: _run_arrstring_arrfloat,
    Scenario.ARRSTRING_ARRSTRING: _run_arrstring_arrstring,
}


def run(scenario, channel):
    stub = rekcurd_pb2_grpc.RekcurdWorkerStub(channel)
    client = RekcurdWorkerClient(
        host="example.com", port=80, application_name="rekcurd-sample",
        service_level="development")
    client.stub = stub
    try:
        return _IMPLEMENTATIONS[scenario](client)
    except grpc.RpcError as rpc_error:
        return Outcome(Outcome.Kind.RPC_ERROR, rpc_error.code(),
                       rpc_error.details())
