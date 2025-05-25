from django.contrib import admin
from .models import Fish, User, UserFish


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','scientific_name','photo')  # Columnas visibles
    search_fields = ('name', 'scientific_name')                                             # Búsqueda por campos                             # Filtros en la barra lateral                                                        # Campos solo lectura

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo')  # Mostrar columnas en la lista
    search_fields = ('id','name')      # Campo de búsqueda

@admin.register(UserFish)
class UserFishAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = (
        'user', 
        'fish', 
        'captured'
    )
    # Campos que permiten buscar registros
    search_fields = ('name', 'scientific_name')  # Corregir si "username" es el campo correcto
    # Campos para filtrar en la lista
    list_filter = ('captured',)  # Debe ser una tupla o lista (añadido `,` para convertirlo en una tupla)
    # Configuración para los campos que se editan directamente en la lista
    list_editable = ('captured',)
    # Configuración para mostrar más detalles en la vista de edición