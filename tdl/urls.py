from django.urls import re_path
from . import views

app_name = 'tdl'
urlpatterns = [
    re_path(r'^$', views.index.as_view(), name='index'),
    re_path(r'^index/xhrval(?P<show>[tf]{1})/$', views.show_hide, name='show_hide'),
    re_path(r'^index/xhr/$', views.show_hide_getval, name='show_hide_getval'),
    re_path(r'^task_done/(?P<task_id>\d+)/$', views.task_done, name='task_done'),
    re_path(r'^task_undone/(?P<task_id>\d+)/$', views.task_undone, name='task_undone'),
    re_path(r'^task_edit/(?P<task_id>\d+)/$', views.task_edit.as_view(), name='task_edit'),
    re_path(r'^task_delete/(?P<task_id>\d+)/$', views.task_delete.as_view(), name='task_delete'),
    re_path(r'^new/$', views.new_task.as_view(), name='new_task'),
]
