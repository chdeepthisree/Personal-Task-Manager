

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def task_list(request):
    query = request.GET.get('q')

    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'query': query,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk)

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})