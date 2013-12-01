from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^$', 'skinflint.finance.views.index'),
    ('^quickadd/$', 'skinflint.finance.views.quickadd'),
    ('^stats/$', 'skinflint.finance.views.stats_summary'),
    ('^add_budget/$', 'skinflint.finance.views.add_budget'),
    ('^add_income/$', 'skinflint.finance.views.add_income'),
    ('^budgets/(?P<id>\d+)/$', 'skinflint.finance.views.budget'),
    ('^budgets/(?P<id>\d+)/add_expense/$',
     'skinflint.finance.views.add_expense'),
    ('^budgets/(?P<id>\d+)/transfer/$', 'skinflint.finance.views.transfer'),
    ('^budgets/(?P<id>\d+)/edit/$', 'skinflint.finance.views.edit_budget'),
    ('^accounts/', include('djangowind.urls')),
    (r'^admin/(.*)', include(admin.site.urls)),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
