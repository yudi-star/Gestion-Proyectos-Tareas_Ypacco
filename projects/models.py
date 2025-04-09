from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", verbose_name="Propietario")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", verbose_name="Proyecto")
    title = models.CharField(max_length=200, verbose_name="Título de la Tarea")
    description = models.TextField(blank=True, verbose_name="Descripción")
    due_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridad")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"