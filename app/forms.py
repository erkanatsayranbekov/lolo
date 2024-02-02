from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=15,required=True,widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Номер телефона'}),label='Номер телефона')
    birth_date = forms.CharField(required=True,widget=forms.DateInput(attrs={'class': 'input','type':'date'}),label='Дата рождения')
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES,required=True,widget=forms.Select(attrs={'class': 'input'}),label='Пол')
    experience = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Опыт работы'}),label='Опыт работы')
    image = forms.ImageField(required=True,widget=forms.FileInput(attrs={'class': 'input'}),label='Фотография')
    password1 = forms.CharField(label="Пароль",widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Пароль'}),)
    password2 = forms.CharField(label="Подтверждение пароля",widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Подтверждение пароля'}),)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'experience', 'phone', 'birth_date' , 'gender', 'image', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Имя пользователя'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}), 
        }
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Пароль'}))

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','description', 'video_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Заголовок'}),
            'description': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Описание'}),
            'video_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ссылка на видео'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'category', 'cover', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Описание'}),
            'cover': forms.FileInput(attrs={'class': 'input', 'required': ''}, ),
            'category': forms.Select(attrs={'class': 'input', 'value': 'Категория'}),
        }
        
class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Добавьте комментарий', 'cols': 30, 'rows': 10}),
        }