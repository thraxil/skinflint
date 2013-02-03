from models import Expense, Budget
from django.forms import ModelForm
import django.forms


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


class QuickAddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        widgets = {
            'when': django.forms.TextInput(attrs={'size': 10}),
            'amount': django.forms.TextInput(attrs={'size': 6}),
        }
