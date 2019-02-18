from .dummy_app import DummyApp

from rekcurd import RekcurdWorkerServicer
from rekcurd.logger import JsonServiceLogger


app = DummyApp()
app.service_logger = JsonServiceLogger()
Type = RekcurdWorkerServicer.Type
