# drucker-client
Drucker is a framework of serving machine learning module. Drucker makes it easy to serve, manage and integrate your ML models into your existing services. Moreover, Drucker can be used on Kubernetes. This project is a SDK for accessing Drucker service of your ML module. All you need is initializing ```DruckerWorkerClient``` class.

## Parent Project
https://github.com/drucker/drucker-parent

## Components
- [Drucker](https://github.com/drucker/drucker): Serving framework for a machine learning module.
- [Drucker-dashboard](https://github.com/drucker/drucker-dashboard): Management web service for the machine learning models to the drucker service.
- [Drucker-client](https://github.com/drucker/drucker-client) (here): SDK for accessing a drucker service.
- [Drucker-example](https://github.com/drucker/drucker-example): Example of how to use drucker.

### Available methods of ```DruckerWorkerClient```
You need to use an appropriate method for your Drucker service. The methods are generated according to the input and output formats. *V* is the length of feature vector. *M* is the number of classes. If your algorithm is a binary classifier, you set *M* to 1. If your algorithm is a multi-class classifier, you set *M* to the number of classes.

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

### Run it
```
$ sh start.sh
```

## Drucker on Kubernetes
https://github.com/drucker/drucker-parent/tree/master/docs/Installation.md
