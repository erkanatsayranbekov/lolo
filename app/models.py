from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )

    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Пол')
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name='Аватар')
    experience = models.TextField(blank=True, null=True, verbose_name='Опыт работы')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
class Catergory(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name

class Course(models.Model):
    category = models.ForeignKey(Catergory, on_delete=models.CASCADE, related_name='get_courses')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='course_images/')
    is_ready = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(CustomUser, related_name="liked_posts")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        
    def __str__(self):
        return f'{self.name} ({self.author.first_name} {self.author.last_name})' 

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_link = models.CharField(max_length=2550)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='get_lessons') 
    status = models.CharField(choices=[('W', 'В процессе'), ('C', 'Завершен')], max_length=1, default='W')
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f'{self.pk}) {self.course.name}'
    
class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='get_enrollments')
    status = models.CharField(choices=[('W', 'В процессе'), ('C', 'Завершен')], max_length=1)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.course.name})'
    
class Rate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])
    
    def __str__(self):
        return self.rate
    
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"