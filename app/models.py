from django.db import models

class Prices(models.Model):

    company = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False,)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adj_close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '%s %s %s %s %s %s %s %s'% (self.company, self.date, self.open, self.high, self.low, self.close, self.adj_close, self.volume)

