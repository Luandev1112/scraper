from django.db import models

class Request(models.Model):
	# uid=models.Foreignkey('auth.User')
	username=models.CharField(max_length=200)
	fname=models.CharField(max_length=200)
	lname=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	password=models.CharField(max_length=200)
	rpassword=models.CharField(max_length=200)

class Txns(models.Model):
	id = models.AutoField(primary_key=True)
	txn_hash = models.CharField(max_length=255)
	method = models.CharField(max_length=50)
	block = models.BigIntegerField()
	age = models.DateTimeField()
	txn_from = models.CharField(max_length=255)
	txn_to = models.CharField(max_length=255)
	value = models.FloatField()
	txn_fee = models.FloatField()

class Transfers(models.Model):
    id=models.AutoField(primary_key=True)
    txn_hash=models.CharField(max_length=255)
    age = models.DateTimeField()
    txn_from = models.CharField(max_length=255)
    txn_to = models.CharField(max_length=255)
    value = models.FloatField()
    transfer_type = models.CharField(max_length=255)
    token = models.CharField(max_length=255)