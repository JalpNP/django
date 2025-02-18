from django.urls import path
from .views import student_form, student_list, update_student, delete_student, products_view, edit_product, delete_product, add_product

urlpatterns = [
    path('', student_form, name='student-form'),
    path('students/', student_list, name='student-list'),
    path('students/update/<str:student_id>/', update_student, name='update-student'),
    path('students/delete/<str:student_id>/', delete_student, name='delete-student'),
    path("products/", products_view, name="products-view"),
    path("products/edit/<int:product_id>/", edit_product, name="edit-product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete-product"),
     path("products/add/", add_product, name="add-product"),
]