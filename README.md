# Django Rest API Buit in Rest framework and mongodatabase


# Requirements.
Pyhton
Django
Virtual Env Creation
Mongodb (mongo or mongod service)


# Installation
Install Python ( Above that 3.5 version)
Install latest django

DEPENDENCIES-
Django==2.1
django-cors-headers==2.4.0 ( To allow cors header for local testing)
django-rest-framework-mongoengine==3.3.1 ( Mongoengine ORM)
djangorestframework==3.8.2
mongoengine==0.15.3
pkg-resources==0.0.0
pymongo==3.7.1
pytz==2018.5
six==1.11.0
uuid==1.30 (Unique uuid generation)


Running-
sudo service mongod restart ( Start Mongo database in localhost : port, ex- 127.0.0.1:27017)
install pip packages with install requirements.txt
python manage.py runserver



#Testing tool
Postman

Most important code files don't have documentation or comments to explain implementation and decisions.

https://github.com/nitinanytime/wallet_api_git/blob/fd8378479ef3b0cd3cc3c65ae6119206be3d8c8d/tr_api/transaction/views.py#L120

All the dependent functions are written in one file 'views'. This is not a correct way to structure code for readability and it is not easily modifiable.

