from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path("user/<int:user_id>/", views.pokedex),
    path("edit/<int:user_id>/", views.edit,name='edit'),
    path('list_user_fishes/<int:user_id>/', views.edit_user_fish, name='list_user_fish'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)