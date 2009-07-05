from models import *
from django.contrib import admin

class BudgetAdmin(admin.ModelAdmin): pass
admin.site.register(Budget,BudgetAdmin)

class IncomeAdmin(admin.ModelAdmin): pass
admin.site.register(Income,IncomeAdmin)

class ExpenseAdmin(admin.ModelAdmin): pass
admin.site.register(Expense,ExpenseAdmin)
