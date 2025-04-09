from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from django.utils import timezone

# Vistas para Proyectos

@login_required
def project_list(request):
    """Vista para listar todos los proyectos"""
    projects = Project.objects.filter(owner=request.user).order_by('-created_date')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    """Vista para ver el detalle de un proyecto y sus tareas"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.all().order_by('due_date')
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, '¡El nombre del proyecto es obligatorio!')
            return render(request, 'projects/project_form.html')

        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user
        )
        messages.success(request, '¡Proyecto creado exitosamente!')
        return redirect('project_detail', pk=project.pk)

    return render(request, 'projects/project_form.html')

@login_required
def project_update(request, pk):
    """Vista para actualizar un proyecto existente"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, 'Project name is required!')
            return render(request, 'projects/project_form.html', {'project': project})

        project.name = name
        project.description = description
        project.save()

        messages.success(request, 'Project updated successfully!')
        return redirect('project_detail', pk=project.pk)

    return render(request, 'projects/project_form.html', {'project': project})

@login_required
def project_delete(request, pk):
    """Vista para eliminar un proyecto"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('project_list')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})

# Vistas para Tareas

@login_required
def task_create(request, project_id):
    """Vista para crear una nueva tarea en un proyecto"""
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        if not title:
            messages.error(request, '¡El título de la tarea es obligatorio!')
            return render(request, 'projects/task_form.html', {'project': project})

        # Crear la tarea
        Task.objects.create(
            project=project,
            title=title,
            description=description,
            due_date=due_date if due_date else None,
            priority=priority
        )

        messages.success(request, '¡Tarea creada exitosamente!')
        return redirect('project_detail', pk=project_id)

    return render(request, 'projects/task_form.html', {'project': project})

@login_required
def task_update(request, pk):
    """Vista para actualizar una tarea existente"""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        if not title:
            messages.error(request, '¡El título de la tarea es obligatorio!')
            return render(request, 'projects/task_form.html', {'task': task, 'project': task.project})

        # Actualizar los datos de la tarea
        task.title = title
        task.description = description
        task.due_date = due_date if due_date else None
        task.priority = priority
        task.status = status
        task.save()

        messages.success(request, '¡Tarea actualizada exitosamente!')
        return redirect('project_detail', pk=task.project.pk)

    return render(request, 'projects/task_form.html', {'task': task, 'project': task.project})

@login_required
def task_delete(request, pk):
    """Vista para eliminar una tarea"""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    project_id = task.project.pk

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('project_detail', pk=project_id)

    return render(request, 'projects/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_status(request, pk):
    """Vista para cambiar rápidamente el estado de una tarea"""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    # Cambiar el estado de la tarea
    if task.status == 'pending':
        task.status = 'in_progress'
    elif task.status == 'in_progress':
        task.status = 'completed'
    else:
        task.status = 'pending'

    task.save()
    return redirect('project_detail', pk=task.project.pk)