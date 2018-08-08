from mongoengine import Document, fields
import datetime


class Customer(Document):
    uid = fields.StringField(max_length=20, unique=True)
    username = fields.StringField(max_length=50)
    password = fields.StringField(max_length=255, default='')


class Wallet(Document):
    cust_uid = fields.ReferenceField(Customer)
    w_type = fields.StringField(max_length=20, default='regular') #regular and overdraft
    current_balance = fields.FloatField(default=0)


class Transaction(Document):
    txn_uid = fields.StringField(max_length=20, unique=True)
    w_uid = fields.ReferenceField(Wallet)
    txn_type = fields.StringField(max_length=50)# credit or debit
    amount = fields.FloatField(default=0)
    status = fields.StringField(default='success')
    creation_date = fields.DateTimeField(auto_now_add=True)
    modified_date = fields.DateTimeField(auto_now=True)
    closing_balance = fields.FloatField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Transaction, self).save(*args, **kwargs)

