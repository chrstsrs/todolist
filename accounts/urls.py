from django.contrib import admin
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views as accounts_views

app_name = 'accounts'
urlpatterns = [
    re_path(r'^signup/$', accounts_views.signup, name='signup'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt', success_url='/accounts/reset/done/'
    ), name='password_reset'),
    re_path(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
            name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html', success_url='/accounts/reset/complete/'),
            name='password_reset_confirm'),
    re_path(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    re_path(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                                           success_url='/accounts/settings/password/done/'), name='password_change'),
    re_path(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
            name='password_change_done'),
]
