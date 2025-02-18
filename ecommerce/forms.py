from django import forms
 
class StudentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    age = forms.IntegerField(label="Age")
    department = forms.CharField(max_length=100, label="Department")

class ProductForm(forms.Form):
    title = forms.CharField(max_length=255)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = forms.URLField()