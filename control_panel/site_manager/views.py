from django.shortcuts import render_to_response
from control_panel.site_manager.models import User, Domain, Website

def index(request):
    return render_to_response('site_manager/index.html')

def users(request):
    users = User.objects.all()
    selected = User.objects.get(id=1)
    return render_to_response('site_manager/users.html', 
        {'users': users, 'selected': selected})

def websites(request):
    websites = Website.objects.all()
    domains = Domain.objects.all()
    return render_to_response('site_manager/websites.html', {'websites': websites})

def activity(request):
    return render_to_response('site_manager/activity.html')
