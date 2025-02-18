from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from .forms import StudentForm, ProductForm
import json
import os
from django.conf import settings
from bson.objectid import ObjectId

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
collection = db["students"]

json_file_path = os.path.join(settings.BASE_DIR, "ecommerce/static/products.json")


def load_products():
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_products(data):
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


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


def products_view(request):
    products_data = load_products()
    products = products_data.get("products", [])
    return render(request, "products.html", {"products": products})


def edit_product(request, product_id):
    products_data = load_products()
    products = products_data.get("products", [])

    product = next((p for p in products if p["id"] == int(product_id)), None)
    if not product:
        return HttpResponse("Product not found", status=404)

    if request.method == "POST":
        product["title"] = request.POST["title"]
        product["price"] = int(request.POST["price"])
        product["thumbnail"] = request.POST["thumbnail"]

        save_products(products_data)
        return redirect("products-view")

    return render(request, "edit_product.html", {"product": product})


def delete_product(request, product_id):
    products_data = load_products()
    products = products_data.get("products", [])

    updated_products = [p for p in products if p["id"] != int(product_id)]
    products_data["products"] = updated_products

    save_products(products_data)
    return redirect("products-view")

def add_product(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = int(request.POST["price"])
        thumbnail = request.POST["thumbnail"]

        products_data = load_products()
        products = products_data.get("products", [])
        last_id = max([product["id"] for product in products], default=0)
        new_product = {
            "id": last_id + 1,
            "title": title,
            "price": price,
            "thumbnail": thumbnail
        }

        products.append(new_product)
        save_products(products_data)
        return redirect("products-view")

    return render(request, "add_product.html")