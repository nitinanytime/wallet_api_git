import uuid
from tr_api.app.customer.serializers import CustomerSerializer


class CustomerParser(object):

    @classmethod
    def parse_customer_object(cls, customer_object):
        return CustomerSerializer(customer_object).data

    @classmethod
    def parse_customer_object_list(cls, customer_object_list):
        return CustomerSerializer(customer_object_list, many=True).data


#Helper functions
def create_cust_uid():
    x = uuid.uuid4()
    y = x.fields
    return 'C' + 'A' + str(y[0])
