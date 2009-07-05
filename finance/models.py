from django.db import models
from django.forms import ModelForm
from django import forms

class Budget(models.Model):
    name = models.CharField(max_length=256)
    amount = models.IntegerField()
    balance = models.IntegerField()

    class Meta:
        ordering = ('-amount',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/budgets/%d/" % self.id

    def get_transfer_form(self):
        return None

class Income(models.Model):
    label = models.CharField(max_length=256)
    amount = models.IntegerField()
    when = models.DateField()
    budget = models.ForeignKey(Budget)

    class Meta:
        ordering = ('when',)

    def __unicode__(self):
        return "%s <- $%d" % (self.budget.name,self.amount)
    
class Expense(models.Model):
    label = models.CharField(max_length=256,blank=True,null=True)
    amount  = models.IntegerField()
    when = models.DateField()
    budget  = models.ForeignKey(Budget)
    
    class Meta:
        ordering = ('when',)

    def  __unicode__(self):
        return "%s: $%d -> %s"  % (self.label,self.amount,self.budget.name)


