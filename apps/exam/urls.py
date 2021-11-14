from django.urls import path, re_path
from .import views

app_name = 'exam'

urlpatterns = [
    re_path(
        r'(?P<exam_uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})|(^(?![\s\S])))',
        views.ExamView.as_view(),
        name='do-exam'
    )
]
