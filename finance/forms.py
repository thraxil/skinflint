from models import *

from django.forms import ModelForm

class BudgetForm(ModelForm):
    class Meta:
        model = Budget

class EditBudgetForm(ModelForm):
    class Meta:
        model = Budget
        exclude = ('balance',)

class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = ('budget',)
