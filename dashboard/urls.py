from django.urls import path
from .views import index, update_status, update_url

urlpatterns = [
    path('', index, name='index'),
    path('update_status/<int:id>/', update_status, name='update_status'),
    path('update_url/<int:id>/', update_url, name="question_update_url")
]