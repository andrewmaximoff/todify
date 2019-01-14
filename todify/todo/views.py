from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import Task
from .forms import TaskForm


def save_task_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            data['form_is_valid'] = True
            if request.path.endswith('completed'):
                tasks = Task.objects.filter(owner=request.user).filter(completed=True).order_by('priority')
            else:
                tasks = Task.objects.filter(owner=request.user).filter(completed=False).order_by('priority')
            data['html_task_list'] = render_to_string('todo/includes/partial_task_list.html', {
                'tasks': tasks
            })
        else:
            data['form_is_valid'] = False

    data['html_form'] = render_to_string(
        template_name,
        context={'form': form},
        request=request)
    return JsonResponse(data)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
    else:
        form = TaskForm()
    return save_task_form(request, form, 'todo/includes/partial_task_create.html')


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(instance=task)
    return save_task_form(request, form, 'todo/includes/partial_task_update.html')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = dict()
    if request.method == 'POST':
        completed = task.completed
        task.delete()
        data['form_is_valid'] = True
        if completed:
            tasks = Task.objects.filter(owner=request.user).filter(completed=True).order_by('priority')
        else:
            tasks = Task.objects.filter(owner=request.user).filter(completed=False).order_by('priority')
        data['html_task_list'] = render_to_string(
            'todo/includes/partial_task_list.html',
            {'tasks': tasks}
        )
    else:
        data['html_form'] = render_to_string(
            'todo/includes/partial_task_delete.html',
            context={'task': task},
            request=request,
        )
    return JsonResponse(data)


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).filter(completed=False).order_by('priority')
    return render(request, 'todo/task_list.html', {'tasks': tasks})


@login_required
def task_completed_list(request):
    tasks = Task.objects.filter(owner=request.user).filter(completed=True).order_by('priority')
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'completed': True})


@login_required
def task_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = dict()
    if request.method == 'GET':
        task.completed = True
        task.save()
        tasks = Task.objects.filter(owner=request.user).filter(completed=False).order_by('priority')
        data['html_task_list'] = render_to_string(
            'todo/includes/partial_task_list.html',
            {'tasks': tasks}
        )
    return JsonResponse(data)


@login_required
def ordered_tasks_ajax(request):
    if not request.is_ajax():
        return Http404

    tasks_id = request.GET.getlist('tasks[]')

    # Re-prioritize each task in list
    i = 1
    for task_id in tasks_id:
        task = Task.objects.get(pk=task_id)
        task.priority = i
        task.save()
        i += 1

    data = {'msg': 'OK'}
    return JsonResponse(data)
