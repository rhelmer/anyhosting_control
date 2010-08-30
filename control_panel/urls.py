from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^control_panel/', include('control_panel.foo.urls')),
    (r'^control_panel/$', 'control_panel.site_manager.views.index'),
    (r'^control_panel/users$', 'control_panel.site_manager.views.users'),
    (r'^control_panel/websites$', 'control_panel.site_manager.views.websites'),
    (r'^control_panel/activity$', 'control_panel.site_manager.views.activity'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
