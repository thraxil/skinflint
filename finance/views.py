from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from datetime import datetime,date
from django.template.defaultfilters import slugify
import simplejson
from models import *
from forms import *
from django.core.paginator import Paginator

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name
 
    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items
 
        return rendered_func

@rendered_with('finance/index.html')
def index(request):
    return dict(budgets=Budget.objects.all(),
                total=sum([b.balance for b in Budget.objects.all()]))

@rendered_with('finance/add_income.html')
def add_income(request):
    if request.method == "POST":
        date = request.POST.get('date','')
        if date == '':
            date = datetime.now()
        label = request.POST.get('label','income')
        for k in request.POST.keys():
            if not k.startswith('income_'):
                continue
            bid = k.split('_')[1]
            budget = Budget.objects.get(id=bid)
            amount = int(request.POST.get(k,'0'))
            if amount == 0:
                continue
            income = Income.objects.create(budget=budget,when=date,
                                           amount=amount,label=label)
            budget.balance += amount
            budget.save()
        return HttpResponseRedirect("/")
                                           
    return dict(budgets=Budget.objects.all())
        

@rendered_with('finance/add_budget.html')
def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST) 
        if form.is_valid():
            b = form.save()
            return HttpResponseRedirect('/') 
    else:
        form = BudgetForm() # An unbound form

    return  {'form': form }

@rendered_with('finance/budget.html')    
def budget(request,id):
    budget = get_object_or_404(Budget,id=id)
    return dict(budget=budget,
                addexpenseform=AddExpenseForm({'when':date.today().isoformat()}),
                transferform=budget.get_transfer_form(),
                all_budgets=Budget.objects.all(),
                )

def add_expense(request,id):
    budget = get_object_or_404(Budget,id=id)
    if request.method == "POST":
        form = AddExpenseForm(request.POST) 
        e = form.save(commit=False)
        e.budget = budget
        if e.label == "":
            e.label = "expense"
        if not e.when:
            e.when = datetime.now()
        e.save()
        budget.balance -= e.amount
        budget.save()
    return HttpResponseRedirect('/') 

def transfer(request,id):
    source = get_object_or_404(Budget,id=id)
    if request.method == "POST":
        target = get_object_or_404(Budget,id=request.POST['target'])
        amount = int(request.POST.get('amount','0'))
        when = datetime.now()
        e = Expense.objects.create(budget=source,amount=amount,when=when,
                                   label="transfer to %s" % target.name)
        source.balance -= amount
        i = Income.objects.create(budget=target,amount=amount,when=when,
                                  label="transfer from %s" % source.name)
        target.balance += amount
    return HttpResponseRedirect('/')

    