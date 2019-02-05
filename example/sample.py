#!/usr/bin/python
# -*- coding: utf-8 -*-


from rekcurd_client import RekcurdWorkerClient
from rekcurd_client.logger import logger


host = 'localhost:5000'
client = RekcurdWorkerClient(logger=logger, host=host)

#domain = 'example.com'
#app = 'rekcurd-sample'
#env = 'development'
#client = RekcurdWorkerClient(logger=logger, domain=domain, app=app, env=env)

input = [0,0,0,1,11,0,0,0,0,0,
         0,7,8,0,0,0,0,0,1,13,
         6,2,2,0,0,0,7,15,0,9,
         8,0,0,5,16,10,0,16,6,0,
         0,4,15,16,13,16,1,0,0,0,
         0,3,15,10,0,0,0,0,0,2,
         16,4,0,0]
response = client.run_predict_arrint_arrint(input)
print(response)
