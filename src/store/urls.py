from django.urls import path
from .views import BoxesAPIView,BoxDetailAPIView

urlpatterns = [
    path('boxes/', BoxesAPIView.as_view()),
    path('box/<int:box_id>/', BoxDetailAPIView.as_view()),
]