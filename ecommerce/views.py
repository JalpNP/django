import requests
from django.shortcuts import render

def home(request):
    url = "https://jsonplaceholder.typicode.com/photos"
    response = requests.get(url)
    data = response.json()

    return render(request, "home.html", {"data": data})