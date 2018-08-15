from django.conf.urls import url
from rest_framework_mongoengine import routers as merouters
from tr_api.app.wallet.views import TransactionView
from tr_api.app.customer.views import CustomerView
from django.views.decorators.csrf import csrf_exempt


merouter = merouters.DefaultRouter()

urlpatterns = [


    # GET all customer list POST for creation of customer
    url(r'^customers$', csrf_exempt(CustomerView.customers), name="customer_crud"),
    # GET for customer with id , POST for creation
    url(r'^customers/(?P<c_uid>[0-9A-Z-]+)$', csrf_exempt(CustomerView.get_customer), name="get_customer"),

    # GET for getting all transactions POST for creating a new transaction
    url(r'^customers/(?P<c_uid>[0-9A-Z-]+)/transactions$', TransactionView.customer_transactions, name="customer_transactions"),

    # Enable POST for creating transaction to make it more analytical informative
    url(r'^customers/transactions/create', TransactionView.create_transaction, name="create_transaction"),

    # GET for request to cancel the transaction
    url(r'^customers/(?P<c_uid>[0-9A-Z-]+)/transactions/(?P<txn_uid>[0-9A-Z-]+)/cancel', csrf_exempt(TransactionView.cancel_transaction), name="cancel_transaction"),

]

urlpatterns += merouter.urls




#
# # GET for customer wallet detail
# url(r'^customers/(?P<c_uid>[-\d]+)/wallet', csrf_exempt(TransactionView.get_wallet_details), name="get_wallet_details"),
