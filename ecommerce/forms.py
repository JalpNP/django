from django import forms
 
class StudentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    age = forms.IntegerField(label="Age")
    department = forms.CharField(max_length=100, label="Department")