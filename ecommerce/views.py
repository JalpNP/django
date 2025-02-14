from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from .forms import StudentForm
from django.conf import settings
from bson.objectid import ObjectId

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
collection = db["students"]

def student_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student_data = {
                "name": form.cleaned_data["name"],
                "age": form.cleaned_data["age"],
                "department": form.cleaned_data["department"],
            }
            collection.insert_one(student_data)
            return redirect("student-list")
    else:
        form = StudentForm()
    return render(request, "form.html", {"form": form})

def student_list(request):
    students = list(collection.find({}))
    for student in students:
        student["id"] = str(student.pop("_id"))
    return render(request, "students_list.html", {"students": students})

def update_student(request, student_id):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return HttpResponse("Student not found", status=404)

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            updated_data = {
                "name": form.cleaned_data["name"],
                "age": form.cleaned_data["age"],
                "department": form.cleaned_data["department"],
            }
            collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})
            return redirect("student-list")

    form = StudentForm(initial={"name": student["name"], "age": student["age"], "department": student["department"]})
    return render(request, "form.html", {"form": form, "update": True})

def delete_student(request, student_id):
    collection.delete_one({"_id": ObjectId(student_id)})
    return redirect("student-list")