from django.db import models
from datetime import datetime, timedelta


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

    def negative_balance(self):
        return self.balance < 0

    def ledger(self, days=365):
        """ return all expenses and incomes in the time frame listed,
        ordered by date """
        cutoff = datetime.now() - timedelta(days=days)
        expenses = list(Expense.objects.filter(budget=self, when__gte=cutoff))
        incomes = list(Income.objects.filter(budget=self, when__gte=cutoff))
        together = expenses + incomes
        together.sort(lambda a, b: cmp(b.when, a.when))
        running_total = self.balance
        for entry in together:
            entry.running_total = running_total
            if entry.is_expense():
                running_total = running_total + entry.amount
            else:
                running_total -= entry.amount
        return together

    def stats(self, days=30):
        """ return total expenses, total incomes, and difference """
        cutoff = datetime.now() - timedelta(days=days)
        expenses = sum([e.amount for e
                        in Expense.objects.filter(budget=self,
                                                  when__gte=cutoff)])
        incomes = sum([i.amount for i
                       in Income.objects.filter(budget=self,
                                                when__gte=cutoff)])
        return dict(expenses=expenses, incomes=incomes, net=incomes - expenses,
                    avg=(float(incomes - expenses) / days))


class Income(models.Model):
    label = models.CharField(max_length=256)
    amount = models.IntegerField()
    when = models.DateField()
    budget = models.ForeignKey(Budget)

    class Meta:
        ordering = ('when',)

    def __unicode__(self):
        return "%s <- $%d" % (self.budget.name, self.amount)

    # handy for ledger views
    def is_expense(self):
        return False

    def is_income(self):
        return True


class Expense(models.Model):
    label = models.CharField(max_length=256, blank=True, null=True)
    amount = models.IntegerField()
    when = models.DateField()
    budget = models.ForeignKey(Budget)

    class Meta:
        ordering = ('when',)

    def __unicode__(self):
        return "%s: $%d -> %s" % (self.label, self.amount, self.budget.name)

    # handy for ledger views
    def is_expense(self):
        return True

    def is_income(self):
        return False


def ledger(days=30):
    """ return all expenses and incomes in the time frame listed,
    ordered by date """
    cutoff = datetime.now() - timedelta(days=days)
    expenses = list(Expense.objects.filter(when__gte=cutoff))
    incomes = list(Income.objects.filter(when__gte=cutoff))
    together = expenses + incomes
    together.sort(lambda a, b: cmp(b.when, a.when))
    running_total = sum([b.balance for b in Budget.objects.all()])
    for entry in together:
        entry.running_total = running_total
        if entry.is_expense():
            running_total = running_total + entry.amount
        else:
            running_total -= entry.amount
    return together


def stats(days=30):
    """ return total expenses, total incomes, and difference """
    cutoff = datetime.now() - timedelta(days=days)
    expenses = sum([e.amount for e
                    in Expense.objects.filter(
                        when__gte=cutoff).exclude(
                            label__icontains="transfer")])
    incomes = sum([i.amount for i
                   in Income.objects.filter(
                       when__gte=cutoff).exclude(label__icontains="transfer")])
    return dict(expenses=expenses, incomes=incomes, net=incomes - expenses,
                avg=(float(incomes - expenses) / days))
