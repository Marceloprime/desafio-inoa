from django.db import models

# Create your models here.
class Price(models.Model):
    symbol = models.CharField(max_length=10,default='')
    current_value = models.DecimalField(max_digits=12,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.symbol +' - '+ str(self.date)

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    website = models.URLField()
    currency = models.CharField(max_length=5)
    current_quote = models.ForeignKey(Price,on_delete=models.CASCADE)
    limit_inferior = models.FloatField(default=-1.00)
    limit_superior = models.FloatField(default=-1.00)
    trend = models.CharField(max_length=7,default='neutral')
    historic = models.ManyToManyField(Price,related_name="stocks_historic",blank=True)

    def __str__(self):
        return self.symbol
