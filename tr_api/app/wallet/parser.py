import uuid
from tr_api.app.wallet.serializers import *
from tr_api.core.constant import WALLET_LIMIT


# Random generation of transaction uid, Prefix can be cnange accroding to year and month
def create_txn_uid():
    x = uuid.uuid4()
    y = x.fields
    return 'T' + 'X' + str(y[0])

# check validity of new balance which is going to take place after this transaction
def get_new_balance(w_object, txn_type, amount):
    """
    :param w_object:
    :param txn_type:
    :param amount:
    :return: new_balance if valid, or None
    """
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


class WalletParser(object):

    # Parse wallet and transaction objects to a seliarize json
    def parse_wallet_with_transaction(w_object=None, txn_obj=None, txn_obj_list=None):
        output = {}

        if w_object:
            w_serilizer = WalletSerializer(w_object)
            output['w_object'] = w_serilizer.data

        if txn_obj:
            t_serializer = TransactionSerializer(txn_obj)
            output['txn_obj'] = t_serializer.data

        if txn_obj_list:
            t_serializer = TransactionSerializer(txn_obj_list, many=True)
            output['txn_objects'] = t_serializer.data

        return output

