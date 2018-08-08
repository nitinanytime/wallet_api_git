from rest_framework_mongoengine import viewsets as meviewsets
from tr_api.transaction.serializers import TransactionSerializer, WalletSerializer, CustomerSerializer
from rest_framework.decorators import api_view
from tr_api.django_rest_params.decorators import params
from tr_api.core.response_parser import ResponseParser
from tr_api.transaction.models import *
from tr_api.core.constant import *
import uuid


class TransactionView(meviewsets.ModelViewSet):

    @api_view(["POST"])
    @params(w_type = WALLET_TYPE_OPTION)
    def create_or_get_wallet(request, w_type):
        request_param = request.data
        result = {}

        try:
            customer_object = Customer.objects.get(username=request_param[USER_NAME])
            try:
                w_object = Wallet.objects.get(cust_uid=customer_object)
            except:
                # create wallet
                new_wallet_object = Wallet(cust_uid=customer_object, w_type=request_param['w_type'])
                new_wallet_object.save()
            result = {USER_NAME: customer_object.username, 'uid': customer_object.uid}
        except:
            #create customer
            customer_object = Customer(username=request_param[USER_NAME], uid = create_cust_uid(), password= 'XYZ' )
            customer_object.save()

            #create wallet
            new_wallet_object = Wallet(cust_uid=customer_object, w_type=request_param['w_type'])
            new_wallet_object.save()

            result = {USER_NAME: customer_object.username, 'uid' : customer_object.uid }

        return ResponseParser.getParsedSuccessMessage(result, message='Successfully customer created.')



    @api_view(["POST"])
    @params(amount=int, txn_type=TYPE_OPTION, c_uid=str)
    def create_transaction(request, amount, txn_type, c_uid):

        # get wallet and validate balance
        w_object = get_wallet_object(c_uid)
        new_balance = get_new_balance(w_object, txn_type, amount)

        if new_balance:
            new_transaction_object = Transaction(txn_uid=create_txn_uid(), w_uid=w_object, txn_type=txn_type, amount=amount, closing_balance = new_balance)
            new_transaction_object.save()

            w_object.current_balance = new_balance
            w_object.save()

            output = parse_wallet_with_transaction(w_object=w_object, txn_obj=new_transaction_object)
            return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transaction Created.')
        else:
            return ResponseParser.getParsedErrorMessage('This will cause the minimum balance limit error.')

    @api_view(["GET"])
    @params(c_uid=str)
    def get_all_transaction(request, c_uid):

        try:
            w_object = get_wallet_object(c_uid)

            transactions = Transaction.objects.filter(w_uid=w_object).order_by('-modified_date')

            output = parse_wallet_with_transaction(w_object=w_object, txn_obj_list=transactions)
            return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transactions listed.')
        except Exception as ex:
            print(ex)
            return ResponseParser.getParsedErrorMessage('Error caused in server, invalid txn_uid')



    @api_view(["GET"])
    def get_all_registrations(request):
        c_objects = Customer.objects.all()
        output = CustomerSerializer(c_objects, many=True).data
        return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transactions listed.')

    @api_view(["GET"])
    @params(txn_uid=str)
    def cancel_transaction(request, txn_uid):
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

                output = parse_wallet_with_transaction(w_object=w_object, txn_obj=transaction_object)
                return ResponseParser.getParsedSuccessMessage(output, message='Successfully Transactions listed.')
            else:
                return ResponseParser.getParsedErrorMessage('Transaction is in already cancelled state.')

        except Exception as ed:
            return ResponseParser.getParsedErrorMessage('Error caused in server, invalid txn_uid')



#Helper functions
def create_cust_uid():
    x = uuid.uuid4()
    y = x.fields
    return 'C' + 'A' + str(y[0])

def create_txn_uid():
    x = uuid.uuid4()
    y = x.fields
    return 'T' + 'X' + str(y[0])


# Parser and support functions
def get_wallet_object(cust_uid):
    c_object = Customer.objects.get(uid=cust_uid)
    return Wallet.objects.get(cust_uid=c_object)

def get_new_balance(w_object, txn_type, amount):
    last_balance = w_object.current_balance
    new_balance = None
    minimun_balance = WALLET_LIMIT[w_object.w_type]

    if txn_type == 'debit':
        new_balance = last_balance - amount

    if txn_type == 'credit':
        new_balance = last_balance + amount

    print (new_balance, minimun_balance)
    if not new_balance < minimun_balance:
        return new_balance
    else:
        return None

def parse_wallet_with_transaction(w_object=None, txn_obj=None, txn_obj_list= None):
    output = {}

    if w_object:
        w_serilizer = WalletSerializer(w_object)
        output['w_object'] = w_serilizer.data

    if txn_obj:
        t_serializer = TransactionSerializer(txn_obj)
        output['txn_obj'] = t_serializer.data

    if txn_obj_list:
        t_serializer = TransactionSerializer(txn_obj_list, many=True)
        output['txn_objects'] =t_serializer.data

    return output