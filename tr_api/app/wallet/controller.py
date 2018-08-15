from tr_api.app.wallet.serializers import *
from tr_api.app.wallet.parser import WalletParser, get_new_balance, create_txn_uid
from tr_api.app.customer.controller import CustomerController


class WalletController(object):

    # create wallet for customer
    @classmethod
    def create_wallet(cls, cust_object, w_type):
        """
        :param cust_object:
        :param w_type:
        :return: wallet_object
        """
        wallet_object = Wallet(cust_uid=cust_object, w_type=w_type).save()
        return wallet_object

    # get wallet object for customer uid
    @classmethod
    def get_wallet_object(cls, c_uid):
        """
        :param c_uid:
        :return: wallet_object
        """
        customer_object = CustomerController.get_customer_object(c_uid)
        print (customer_object.uid)
        return Wallet.objects.get(cust_uid=customer_object)

    @classmethod
    def create_transaction(cls, amount, txn_type,  new_balance, w_object):
        """
        :param amount:
        :param txn_type:
        :param new_balance:
        :param w_object:
        :return: transaction_object
        """
        #create new transaction
        new_transaction_object = Transaction(txn_uid=create_txn_uid(),
                                             w_uid=w_object,
                                             txn_type=txn_type,
                                             amount=amount,
                                             closing_balance=new_balance).save()

        # update the wallet balance
        w_object.current_balance = new_balance
        w_object.save()
        return w_object, new_transaction_object

    # Parser and support functions
    @classmethod
    def get_transactions(cls, c_uid=None, wallet_object=None):
        """
        :param c_uid:
        :param wallet_object:
        :return: list of transaction_objects related to customer associated with wallet.
        """
        if c_uid:
            wallet_object = CustomerController.get_customer_object(c_uid)
        if wallet_object:
            txn_objects = Transaction.objects.filter(w_uid=wallet_object).order_by('-modified_date')
            return txn_objects
        else:
            return None

