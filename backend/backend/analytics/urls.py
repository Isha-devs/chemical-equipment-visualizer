from django.urls import path
from .views import UploadCSVView, UploadHistoryView



urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('history/', UploadHistoryView.as_view()),
]

