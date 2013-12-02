from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Budget, ledger, stats, Income, Expense
from .forms import QuickAddExpenseForm, BudgetForm, AddExpenseForm
from .forms import EditBudgetForm


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(LoggedInMixin, TemplateView):
    template_name = 'finance/index.html'

    def get_context_data(self):
        return dict(
            budgets=Budget.objects.all(),
            ledger=ledger(days=30),
            stats_week=stats(days=7),
            stats_month=stats(days=30),
            stats_year=stats(days=365),
            quickadd=QuickAddExpenseForm(
                {'when': date.today().isoformat()}),
            total=sum([b.balance for b in Budget.objects.all()]))


class StatsView(TemplateView):
    template_name = 'finance/stats.html'

    def get_context_data(self):
        return dict(budgets=Budget.objects.all(),
                    stats_week=stats(days=7),
                    stats_month=stats(days=30),
                    stats_year=stats(days=365),
                    total=sum([b.balance for b in Budget.objects.all()]))


class AddIncomeView(LoggedInMixin, View):
    template_name = 'finance/add_income.html'

    def post(self, request):
        date = request.POST.get('date', '')
        if date == '':
            date = datetime.now()
        label = request.POST.get('label', 'income')
        for k in request.POST.keys():
            if not k.startswith('income_'):
                continue
            bid = k.split('_')[1]
            budget = Budget.objects.get(id=bid)
            amount = int(request.POST.get(k, '0'))
            if amount == 0:
                continue
            Income.objects.create(budget=budget, when=date,
                                  amount=amount, label=label)
            budget.balance += amount
            budget.save()
        return HttpResponseRedirect("/")

    def get(self, request):
        return render(request, self.template_name,
                      dict(budgets=Budget.objects.all()))


class AddBudgetView(LoggedInMixin, CreateView):
    model = Budget
    form = BudgetForm
    template_name = 'finance/add_budget.html'
    success_url = '/'


class BudgetView(LoggedInMixin, DetailView):
    model = Budget
    context_object_name = 'budget'

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)
        budget = context['budget']
        context['addexpenseform'] = AddExpenseForm(
            {'when': date.today().isoformat()})
        context['transferform'] = budget.get_transfer_form()
        context['all_budgets'] = Budget.objects.all()
        context['stats_week'] = budget.stats(days=7)
        context['stats_month'] = budget.stats(days=30)
        context['stats_year'] = budget.stats(days=365)
        return context


class EditBudgetView(LoggedInMixin, UpdateView):
    model = Budget
    template_name = 'finance/edit_budget.html'
    form = EditBudgetForm


class AddExpenseView(LoggedInMixin, View):
    def post(self, request, id):
        budget = get_object_or_404(Budget, id=id)
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


class QuickAddView(LoggedInMixin, View):
    def post(self, request):
        form = QuickAddExpenseForm(request.POST)
        e = form.save(commit=False)
        if e.label == "":
            e.label = "expense"
        if not e.when:
            e.when = datetime.now()
        e.save()
        e.budget.balance -= e.amount
        e.budget.save()
        return HttpResponseRedirect('/')


class TransferView(LoggedInMixin, View):
    def post(self, request, id):
        source = get_object_or_404(Budget, id=id)
        target = get_object_or_404(Budget, id=request.POST['target'])
        amount = int(request.POST.get('amount', '0'))
        when = datetime.now()
        Expense.objects.create(budget=source, amount=amount, when=when,
                               label="transfer to %s" % target.name)
        source.balance -= amount
        Income.objects.create(budget=target, amount=amount, when=when,
                              label="transfer from %s" % source.name)
        target.balance += amount
        source.save()
        target.save()
        return HttpResponseRedirect('/')
