from django.contrib import admin
from .models import Project, Task

# Acción personalizada para tareas
@admin.action(description="Marcar tareas seleccionadas como completadas")
def marcar_completadas(modeladmin, request, queryset):
    queryset.update(status='completed')

# Inline mejorado para mostrar más campos de las tareas
class TaskInline(admin.TabularInline):
    model = Task
    fields = ('title', 'priority', 'status', 'due_date')
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_date')
    search_fields = ('name', 'description')
    list_filter = ('created_date', 'owner')
    date_hierarchy = 'created_date'
    inlines = [TaskInline]
    readonly_fields = ('created_date',)
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('name', 'description')
        }),
        ('Datos del Propietario', {
            'fields': ('owner', 'created_date')
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'due_date')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status', 'due_date', 'project')
    list_editable = ('priority', 'status', 'due_date')
    date_hierarchy = 'due_date'
    actions = [marcar_completadas]
    list_per_page = 20

# Personalización de los títulos del admin
admin.site.site_header = "Gestor de Proyectos y Tareas"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Administrador"