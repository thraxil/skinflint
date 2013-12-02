from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings
from skinflint.finance import views
admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^$', views.IndexView.as_view()),
    ('^quickadd/$', 'skinflint.finance.views.quickadd'),
    ('^stats/$', views.StatsView.as_view()),
    ('^add_budget/$', views.AddBudgetView.as_view()),
    ('^add_income/$', views.AddIncomeView.as_view()),
    ('^budgets/(?P<pk>\d+)/$', views.BudgetView.as_view()),
    ('^budgets/(?P<id>\d+)/add_expense/$',
     'skinflint.finance.views.add_expense'),
    ('^budgets/(?P<id>\d+)/transfer/$', 'skinflint.finance.views.transfer'),
    ('^budgets/(?P<pk>\d+)/edit/$', views.EditBudgetView.as_view()),
    ('^accounts/', include('djangowind.urls')),
    (r'^admin/(.*)', include(admin.site.urls)),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
