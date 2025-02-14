from django.urls import path
from .views import student_form, student_list, update_student, delete_student

urlpatterns = [
    path('', student_form, name='student-form'),
    path('students/', student_list, name='student-list'),
    path('students/update/<str:student_id>/', update_student, name='update-student'),
    path('students/delete/<str:student_id>/', delete_student, name='delete-student'),
]