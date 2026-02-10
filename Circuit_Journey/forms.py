from .models import *
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class Createblogform(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full mt-2 p-3 rounded-xl border border-gray-300 bg-white text-gray-900 "
                     "placeholder-gray-500 focus:border-green-600 focus:ring-2 focus:ring-green-600",
            "placeholder": "Enter your blog title…",
            "autocomplete": "off",
        })
    )
    thumbnail = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            "class": "block w-full mt-2 p-3 rounded-xl border border-gray-300 bg-white text-gray-900 "
                     "focus:border-green-600 focus:ring-2 focus:ring-green-600",
            "accept": "image/*",
        })
    )
    video = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "block w-full mt-2 p-3 rounded-xl border border-gray-300 bg-white text-gray-900 "
                     "focus:border-green-600 focus:ring-2 focus:ring-green-600",
            "accept": "video/mp4,video/webm,video/quicktime,video/x-msvideo,video/x-ms-wmv",
        })
    )
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.Select(attrs={
            "class": "w-full mt-2 p-3 rounded-xl border border-gray-300 bg-white text-gray-900 "
                     "focus:border-green-600 focus:ring-2 focus:ring-green-600",
        })
    )

    class Meta:
        model = Blog
        fields = ["title", "thumbnail", "video", "body", "category"]
        widgets = {
            "body": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5 block w-full mt-2 border border-gray-300 rounded-xl "
                             "focus:ring-2 focus:ring-green-600"
                },
                config_name="extends",
            )
        }
        
class Commentform(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "add comment"}))
    
    class Meta:
        model = Comments
        fields = ['body']