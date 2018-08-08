__author__ = 'nitindwivedi'


#Import Libraries. models, views, functions, etc.

import json


class ResponseParser(object):

    @classmethod
    def getParsedErrorMessage(cls, string):
        return cls.getHTTPResponseForDictionary({'success':0, 'message':string, 'status': "E01"})

    @classmethod
    def getParsedSuccessMessage(cls, data, message, status=200):
        return cls.getHTTPResponseForDictionary({'success':1, 'data':data, 'status':status, 'message':message})

    @classmethod
    def getParsedSuccessMessageWithDict(cls, data, status, message):
        return cls.getHTTPResponseForDictionary({'success': '0', 'data': data, 'status': status, 'message': message})

    @classmethod
    def getErrorMessage(cls, errorMessage, errorCode):
        ErrorMessage = str(errorCode)
        return cls.getParsedErrorMessage(ErrorMessage)

    @classmethod
    def getErrorMessage(cls, errorMessage, errorCode):
        ErrorMessage = errorMessage + str(errorCode)
        return cls.getParsedErrorMessage(ErrorMessage)

    @classmethod
    def getSpecificErrorMessage(cls, errorCode):
        ErrorMessage = str(errorCode)
        return cls.getParsedErrorMessage(ErrorMessage)

    @classmethod
    def getHTTPResponseForDictionary(cls ,dictionary):
        from django.http import JsonResponse
        # httpResponse = HttpResponse(json.dumps(dictionary, cls=json.JSONEncoder, indent=2), content_type="application/json")
        httpResponse = JsonResponse(dictionary, safe=False, content_type="application/json")
        httpResponse = cls.add_access_control_headers(httpResponse)
        return httpResponse


    @classmethod
    def add_access_control_headers(cls, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response

    @classmethod
    def return_response_json_from_file(cls, filename):

        json_data = open('static/constant/'+ filename, 'rt', encoding='utf-8')
        data1 = json.load(json_data)

        return cls.getHTTPResponseForDictionary({'success': '1', 'data': data1, 'status': 'SE01', 'message': 'success'})

