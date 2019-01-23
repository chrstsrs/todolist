from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse, response
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task, Preferences
from .forms import NewTaskForm


class index(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tdl/index.html'
    context_object_name = 'tasks'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('pk')


@login_required
def show_hide(request, show):
    user = request.user.pk
    preferences = get_object_or_404(Preferences, user=user)
    preferences.show_all = (show == "t")
    preferences.save()
    return HttpResponse(preferences.show_all)


@login_required
def show_hide_getval(request):
    user = request.user
    preferences, _ = Preferences.objects.get_or_create(
        user=user, defaults={'user': user, 'show_all': False})
    return HttpResponse(preferences.show_all)


class new_task(LoginRequiredMixin, CreateView):
    model = Task
    form_class = NewTaskForm
    template_name = 'tdl/new_task.html'
    context_object_name = 'form'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.issued_by = self.request.user
        task.save()
        return redirect('tdl:index')


class task_edit(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = NewTaskForm
    template_name = 'tdl/edit.html'
    context_object_name = 'form'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('tdl:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(issued_by=self.request.user)


class task_delete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tdl:index')
    pk_url_kwarg = 'task_id'
    template_name = 'tdl/delete_confirm.html'
    context_object_name = 'task'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(issued_by=self.request.user)


@login_required
def task_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.done = True
    task.done_by = request.user
    task.save()
    tasks = Task.objects.all()
    return redirect('tdl:index')


@login_required
def task_undone(request, task_id):
    task = get_object_or_404(Task, pk=task_id, issued_by=request.user)
    task.done = False
    task.save()
    tasks = Task.objects.all()
    return redirect('tdl:index')
