from django.conf.urls import url
from rest_framework_mongoengine import routers as merouters
from tr_api.transaction.views import TransactionView
from django.views.decorators.csrf import csrf_exempt


merouter = merouters.DefaultRouter()

urlpatterns = [


    url(r'^get_wallet', csrf_exempt(TransactionView.create_or_get_wallet), name="get_wallet"),
    url(r'^get_registrations', csrf_exempt(TransactionView.get_all_registrations), name="get_registrations"),
    url(r'^get_all_transaction', TransactionView.get_all_transaction, name="get_all_transaction"),
    url(r'^create_transaction', csrf_exempt(TransactionView.create_transaction), name="create_transaction"),
    url(r'^cancel_transaction', csrf_exempt(TransactionView.cancel_transaction), name="cancel_transaction"),


]

urlpatterns += merouter.urls