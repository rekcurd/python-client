# rekcurd-client

[![Build Status](https://travis-ci.com/rekcurd/drucker-client.svg?branch=master)](https://travis-ci.com/rekcurd/drucker-client)
[![PyPI version](https://badge.fury.io/py/rekcurd-client.svg)](https://badge.fury.io/py/rekcurd-client)
[![codecov](https://codecov.io/gh/rekcurd/drucker-client/branch/master/graph/badge.svg)](https://codecov.io/gh/rekcurd/drucker-client "Non-generated packages only")
[![pypi supported versions](https://img.shields.io/pypi/pyversions/rekcurd-client.svg)](https://pypi.python.org/pypi/rekcurd-client)

Rekcurd client is the project for integrating ML module. Any Rekcurd service is connectable. It can connect the Rekcurd service on Kubernetes.


## Parent Project
https://github.com/rekcurd/drucker-parent


## Components
- [Rekcurd](https://github.com/rekcurd/drucker): Project for serving ML module.
- [Rekcurd-dashboard](https://github.com/rekcurd/drucker-dashboard): Project for managing ML model and deploying ML module.
- [Rekcurd-client](https://github.com/rekcurd/drucker-client) (here): Project for integrating ML module. 


## Installation
From source:

```
git clone --recursive https://github.com/rekcurd/drucker-client.git
cd drucker-client
python setup.py install
```

From [PyPi](https://pypi.org/project/rekcurd_client/) directly:

```
pip install rekcurd_client
```

## How to use
Example code is available [here](./example/sample.py).

```python
from drucker_client import DruckerWorkerClient
from drucker_client.logger import logger


host = 'localhost:5000'
client = DruckerWorkerClient(logger=logger, host=host)

input = [0,0,0,1,11,0,0,0,0,0,
         0,7,8,0,0,0,0,0,1,13,
         6,2,2,0,0,0,7,15,0,9,
         8,0,0,5,16,10,0,16,6,0,
         0,4,15,16,13,16,1,0,0,0,
         0,3,15,10,0,0,0,0,0,2,
         16,4,0,0]
response = client.run_predict_arrint_arrint(input)
```

When you use Kubernetes and deploy Rekcurd service via Rekcurd dashboard, you can access your Rekcurd service like the below.

```python
from drucker_client import DruckerWorkerClient
from drucker_client.logger import logger


domain = 'example.com'
app = 'drucker-sample'
env = 'development'
client = DruckerWorkerClient(logger=logger, domain=domain, app=app, env=env)

input = [0,0,0,1,11,0,0,0,0,0,
         0,7,8,0,0,0,0,0,1,13,
         6,2,2,0,0,0,7,15,0,9,
         8,0,0,5,16,10,0,16,6,0,
         0,4,15,16,13,16,1,0,0,0,
         0,3,15,10,0,0,0,0,0,2,
         16,4,0,0]
response = client.run_predict_arrint_arrint(input)
```

### DruckerWorkerClient
You need to use an appropriate method for your Rekcurd service. The methods are generated according to the input and output formats. *V* is the length of feature vector. *M* is the number of classes. If your algorithm is a binary classifier, you set *M* to 1. If your algorithm is a multi-class classifier, you set *M* to the number of classes.

|method |input: data<BR>(required) |input: option |output: label<BR>(required) |output: score<BR>(required) |output: option |
|:---|:---|:---|:---|:---|:---|
|run_predict_string_string |string |string (json) |string |double |string (json) |
|run_predict_string_bytes |string |string (json) |bytes |double |string (json) |
|run_predict_string_arrint |string |string (json) |int[*M*] |double[*M*] |string (json) |
|run_predict_string_arrfloat |string |string (json) |double[*M*] |double[*M*] |string (json) |
|run_predict_string_arrstring |string |string (json) |string[*M*] |double[*M*] |string (json) |
|run_predict_bytes_string |bytes |string (json) |string |double |string (json) |
|run_predict_bytes_bytes |bytes |string (json) |bytes |double |string (json) |
|run_predict_bytes_arrint |bytes |string (json) |int[*M*] |double[*M*] |string (json) |
|run_predict_bytes_arrfloat |bytes |string (json) |double[*M*] |double[*M*] |string (json) |
|run_predict_bytes_arrstring |bytes |string (json) |string[*M*] |double[*M*] |string (json) |
|run_predict_arrint_string |int[*V*] |string (json) |string |double |string (json) |
|run_predict_arrint_bytes |int[*V*] |string (json) |bytes |double |string (json) |
|run_predict_arrint_arrint |int[*V*] |string (json) |int[*M*] |double[*M*] |string (json) |
|run_predict_arrint_arrfloat |int[*V*] |string (json) |double[*M*] |double[*M*] |string (json) |
|run_predict_arrint_arrstring |int[*V*] |string (json) |string[*M*] |double[*M*] |string (json) |
|run_predict_arrfloat_string |double[*V*] |string (json) |string |double |string (json) |
|run_predict_arrfloat_bytes |double[*V*] |string (json) |bytes |double |string (json) |
|run_predict_arrfloat_arrint |double[*V*] |string (json) |int[*M*] |double[*M*] |string (json) |
|run_predict_arrfloat_arrfloat |double[*V*] |string (json) |double[*M*] |double[*M*] |string (json) |
|run_predict_arrfloat_arrstring |double[*V*] |string (json) |string[*M*] |double[*M*] |string (json) |
|run_predict_arrstring_string |string[*V*] |string (json) |string |double |string (json) |
|run_predict_arrstring_bytes |string[*V*] |string (json) |bytes |double |string (json) |
|run_predict_arrstring_arrint |string[*V*] |string (json) |int[*M*] |double[*M*] |string (json) |
|run_predict_arrstring_arrfloat |string[*V*] |string (json) |double[*M*] |double[*M*] |string (json) |
|run_predict_arrstring_arrstring |string[*V*] |string (json) |string[*M*] |double[*M*] |string (json) |

The input "option" field needs to be a json format. Any style is Ok but we have some reserved fields below.

|Field |Type |Description |
|:---|:---|:---|
|suppress_log_input |bool |True: NOT print the input and output to the log message. <BR>False (default): Print the input and output to the log message.


## Unittest
```
$ python -m unittest
```
