from rest_framework_mongoengine import viewsets as meviewsets
from tr_api.app.customer.controller import CustomerController
from tr_api.app.wallet.controller import WalletController
from rest_framework.decorators import api_view
from tr_api.core.response_parser import ResponseParser

from tr_api.core.constant import *


class CustomerView(meviewsets.ModelViewSet):


    @api_view(["GET"])
    def get_customer(request, c_uid):
        output = CustomerController.get_customer_parsed(c_uid)
        return ResponseParser.getParsedSuccessMessage(output, message='Successfully GET customer_detail created.')


    @api_view(["GET", "POST"])
    def customers(request):

        if request.method == 'GET':
            output = CustomerController.get_customers_parsed()
            return ResponseParser.getParsedSuccessMessage(output, message='Successfully Customer list fetched.')

        if request.method == 'POST':
            request_data = request.data
            cust_object = CustomerController.create_customer(request_data)

            if cust_object:
                w_object = WalletController.create_wallet(cust_object, request_data[WALLET_TYPE])
                return ResponseParser.getParsedSuccessMessage({USER_NAME: cust_object.username, 'uid': cust_object.uid}, message='Successfully GET created.')

            else:
                return ResponseParser.getParsedErrorMessage('Validation Error in Customer creation.')
