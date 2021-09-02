from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from stocks.models import Stock
# Create your models here.
class User(AbstractUser):
    cpf_or_cnpj = models.CharField(max_length=25)
    phone = PhoneNumberField()

    def __str__(self):
        return self.email

class Portfolio(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    portfolio = models.ManyToManyField(Stock,blank=True)

    def  __str__(self):
        return self.name


