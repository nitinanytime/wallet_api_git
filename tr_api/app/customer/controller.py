from tr_api.app.customer.serializers import *
from tr_api.app.customer.parser import *


class CustomerController(object):

    @classmethod
    def create_customer(cls, request_param):
        """
        :param request_param:
        :return: customer_object
        """
        cust_object = None
        cust_form = CustomerForm(request_param)
        print(cust_form.errors)
        if cust_form.is_valid():
            cust_object = Customer(username=cust_form.cleaned_data[USER_NAME],
                                   uid=create_cust_uid(),
                                   password='XXX').save()

        return cust_object

    @classmethod
    def get_customer_object(cls, c_uid):
        """
        :param c_uid:
        :return: customer_object or None(if not found)
        """
        try:
            customer_object = Customer.objects.get(uid=c_uid)
            return customer_object
        except:
            print("NONE")
            return None

    @classmethod
    def get_customer_parsed(cls, c_uid):
        """
        :param c_uid:
        :return: Parsed serilized json for customer object feilds.
        """
        try:
            customer_object = Customer.objects.get(c_uid=c_uid)
            customer_parsed = CustomerParser.parse_customer_object(customer_object)
            return customer_parsed
        except:
            return None

    @classmethod
    def get_customers_parsed(cls, request_param={}):
        # if any filler , apply here
        customers_object_list = Customer.objects.all()

        #Parse the filtered objects
        all_customers_parsed = CustomerParser.parse_customer_object_list(customers_object_list)
        return all_customers_parsed

