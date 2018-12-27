"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', RedirectView.as_view(url='todolist'), name='home'),
    re_path(r'^todolist/', include('tdl.urls', namespace='todolist')),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^favicon.ico/$', RedirectView.as_view(
        url=staticfiles_storage.url('img/favicon.ico'),), name="favicon"),

    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
]
