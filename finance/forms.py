from models import *

from django.forms import ModelForm

class BudgetForm(ModelForm):
    class Meta:
        model = Budget

class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = ('budget',)
