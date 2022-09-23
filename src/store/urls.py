from django.urls import path
from .views import BoxAPIView

urlpatterns = [
    path('box/', BoxAPIView.as_view()),
]