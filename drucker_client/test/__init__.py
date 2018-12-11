import os

from drucker.logger import JsonServiceLogger, JsonSystemLogger
import drucker.drucker_worker_servicer

from drucker_client.test.dummy_app import DummyApp
from drucker_client.logger import logger


os.environ["DRUCKER_TEST_MODE"] = "True"
os.environ["DRUCKER_SETTINGS_YAML"] = "drucker_client/test/test-settings.yml"

app = DummyApp()
service_logger = JsonServiceLogger(app.config)
system_logger = JsonSystemLogger(app.config)
Type = drucker.drucker_worker_servicer.DruckerWorkerServicer.Type
client_logger = logger
