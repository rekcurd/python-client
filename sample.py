#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from core.drucker_worker_client import DruckerWorkerClient

from logger.logger_jsonlogger import SystemLogger
logger = SystemLogger(logger_name="drucker_client")

url = 'localhost:5000'
client = DruckerWorkerClient(logger=logger, url=url)

#domain = 'example.com'
#app = 'drucker-sample'
#env = 'development'
#client = DruckerWorkerClient(logger=logger, domain=domain, app=app, env=env)

input = [0,0,0,1,11,0,0,0,0,0,
         0,7,8,0,0,0,0,0,1,13,
         6,2,2,0,0,0,7,15,0,9,
         8,0,0,5,16,10,0,16,6,0,
         0,4,15,16,13,16,1,0,0,0,
         0,3,15,10,0,0,0,0,0,2,
         16,4,0,0]
response = client.run_predict_arrint_arrint(input)
print(response)