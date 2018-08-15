from rest_framework_mongoengine import viewsets as meviewsets
from tr_api.app.wallet.serializers import TransactionSerializer, WalletSerializer
from tr_api.app.wallet.parser import *
from tr_api.app.wallet.controller import WalletController
from rest_framework.decorators import api_view, action
from tr_api.core.decorators import params
from tr_api.core.response_parser import ResponseParser
from tr_api.app.models import *
from tr_api.core.constant import *
import uuid


class TransactionView(meviewsets.ModelViewSet):

    @api_view(['GET'])
    def customer_transactions(request, c_uid):

        if request.method == 'GET':
            try:
                # get wallet object
                w_object = WalletController.get_wallet_object(c_uid)

                # get list of transactions
                transactions = WalletController.get_transactions(wallet_object=w_object)

                # Parsed output
                output = WalletParser.parse_wallet_with_transaction(w_object=w_object, txn_obj_list=transactions)
                return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transactions listed.')
            except Exception as ex:
                print(ex)
                return ResponseParser.getParsedErrorMessage('Error caused in server, invalid txn_uid')

        if request.method == 'POST':
            request_data = request.data
            transaction_form = TransactionForm(request_data)

            if transaction_form.is_valid():
                txn_type = transaction_form.cleaned_data[TXN_TYPE]
                amount = transaction_form.cleaned_data[AMOUNT]

                # get wallet and validate balance
                w_object = WalletController.get_wallet_object(c_uid)
                new_balance = get_new_balance(w_object, txn_type, amount)

                if new_balance:
                    w_object, new_transaction_object = WalletController.create_transaction(amount, txn_type,
                                                                                           new_balance, w_object)
                    output = WalletParser.parse_wallet_with_transaction(w_object=w_object,
                                                                        txn_obj=new_transaction_object)
                    return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transaction Created.')
                else:
                    return ResponseParser.getParsedErrorMessage('This will cause the minimum balance limit error.')


    @api_view(["GET"])
    def cancel_transaction(request, c_uid, txn_uid):
        try:
            transaction_object = Transaction.objects.get(txn_uid=txn_uid)
            w_object = transaction_object.w_uid

            if transaction_object.status == 'success':
                new_balance = None
                if transaction_object.txn_type == 'debit' :
                    new_balance = get_new_balance(w_object, 'credit' , transaction_object.amount)
                if transaction_object.txn_type == 'credit':
                    new_balance = get_new_balance(w_object, 'debit', transaction_object.amount)

                if new_balance:
                    transaction_object.closing_balance = new_balance
                    transaction_object.status = 'cancelled'
                    transaction_object.save()
                    w_object.current_balance = new_balance
                    w_object.save()
                else:
                    return ResponseParser.getParsedErrorMessage('This will cause the minimum balance limit error.')

                output = WalletParser.parse_wallet_with_transaction(w_object=w_object, txn_obj=transaction_object)
                return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transactions listed.')
            else:
                return ResponseParser.getParsedErrorMessage('Transaction is in already cancelled state.')

        except Exception as ed:
            return ResponseParser.getParsedErrorMessage('Error caused in server, invalid txn_uid')

    @api_view(["POST"])
    @params(amount=int, txn_type=TYPE_OPTION, c_uid=str)
    def create_transaction(request, amount, txn_type, c_uid):

        # get wallet and validate balance
        w_object = WalletController.get_wallet_object(c_uid)
        new_balance = get_new_balance(w_object, txn_type, amount)

        if new_balance:
            w_object, new_transaction_object = WalletController.create_transaction(amount, txn_type, new_balance,
                                                                                   w_object)
            output = WalletParser.parse_wallet_with_transaction(w_object=w_object, txn_obj=new_transaction_object)
            return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transaction Created.')
        else:
            return ResponseParser.getParsedErrorMessage('This will cause the minimum balance limit error.')
