from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^skinflint/', include('skinflint.foo.urls')),
                       ('^$','finance.views.index'),
                       ('^stats/$','finance.views.stats_summary'),
                       ('^add_budget/$','finance.views.add_budget'),
                       ('^add_income/$','finance.views.add_income'),
                       ('^budgets/(?P<id>\d+)/$','finance.views.budget'),
                       ('^budgets/(?P<id>\d+)/add_expense/$','finance.views.add_expense'),
                       ('^budgets/(?P<id>\d+)/transfer/$','finance.views.transfer'),
                       ('^budgets/(?P<id>\d+)/edit/$','finance.views.edit_budget'),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
)
