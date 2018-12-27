from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, response
from .models import Task, Preferences
from .forms import NewTaskForm


@login_required
def index(request):
    tasks = Task.objects.all()
    userid = request.user.pk
    user = request.user
    return render(request, 'tdl/index.html', {'tasks': tasks, 'user': user})


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


@login_required
def new_task(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.issued_by = request.user
            task.save()
            return redirect('tdl:index')
    else:
        form = NewTaskForm()
    return render(request, 'tdl/new_task.html', {'form': form})


@login_required
def task_edit(request, task_id):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            formtask = form.save(commit=False)
            task = Task.objects.get(pk=task_id)
            task.name = formtask.name
            task.description = formtask.description
            task.save()
            return redirect('tdl:index')
    else:
        task = get_object_or_404(Task, pk=task_id, issued_by=request.user)
        form = NewTaskForm(initial={'name': task.name, 'description': task.description})
    return render(request, 'tdl/edit.html', {'form': form})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, issued_by=request.user)
    task.delete()
    return redirect('tdl:index')


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
