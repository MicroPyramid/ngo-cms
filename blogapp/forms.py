from django import forms
from blogapp.models import Category, Post, Contact, Menu, Page, Banner


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "slug"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "short_desc", "category",
                  "is_featured_news", "slug", "description"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "parent", "slug"]


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'slug']


class bannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'short_desc']


class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length=20)
    new_password = forms.CharField(max_length=20)
    re_password = forms.CharField(max_length=20)
