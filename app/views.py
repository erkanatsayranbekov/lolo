from typing import Any
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import *
from .forms import *
from django.core.mail import send_mail
from django.db.models import Avg

class Home(TemplateView):
    template_name = 'home.html'
    
class Dashboard(ListView):
    model = Course
    template_name = 'dashboard.html'
    context_object_name = 'courses'
    

class SignUpWithVerification(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response

class VerificationSuccessView(TemplateView):
    template_name = 'verification_success.html'

class VerificationErrorView(TemplateView):
    template_name = 'verification_error.html'

class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = get_user_model().objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verification_success')
        else:
            return redirect('verification_error')

class Login(LoginView):
    form_class = LoginForm
    next_page = reverse_lazy('home')
    template_name = 'login.html'

class Logout(LogoutView):
    next_page = reverse_lazy('login')

class BecomeCreator(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request):
        request.user.is_creator = True
        request.user.save()
        return redirect('home')

class CreateLesson(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):

        course = Course.objects.get(pk=self.kwargs['course_id'])
        form = self.get_form()
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.video_link = form.cleaned_data['video_link'].replace('/watch?v=', '/embed/') + '?si=3w72S4xQu7dvvp5g'
            lesson.course = course
            lesson.save()
            if 'save_and_add' in self.request.POST:
                return HttpResponseRedirect(reverse_lazy('create_lesson', kwargs={'course_id': course.pk}))
            return HttpResponseRedirect(reverse_lazy('my_courses'))
        return self.render_to_response(self.get_context_data(form=form)) 

class IsCreatorMixin:
    def dispatch(self, request):
        if not request.user.is_creator:
            return redirect('home')
        return super().dispatch(request)

class CreateCourse(LoginRequiredMixin,IsCreatorMixin, CreateView):
    model = Course
    form_class = CourseForm
    login_url = reverse_lazy('login')
    template_name = 'create_course.html'
    success_url = reverse_lazy('create_lesson')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form_lesson'] = LessonForm()
        return context
    
    def form_valid(self, request):
        form = self.get_form()
        if form.is_valid():
            course = form.save(commit=False)
            course.author = self.request.user
            course.save()
            return redirect('create_lesson', course_id=course.pk)
        return self.render_to_response(self.get_context_data(form=form))
    
class MyCourses(ListView):
    model = Course
    template_name = 'my_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(author=self.request.user)

class IsOwenerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class IsLessonOwener:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.course.author != request.user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class DeleteCourse(LoginRequiredMixin, IsOwenerMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Course
    pk_url_kwarg = 'course_id'
    success_url = reverse_lazy('my_courses')

class UpdateCourse(LoginRequiredMixin, IsOwenerMixin, UpdateView):
    login_url = reverse_lazy("login")
    form_class = CourseForm
    model = Course
    template_name = 'update_course.html'
    pk_url_kwarg = 'course_id'
    success_url = reverse_lazy('home')
    
class SetLike(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        if request.user in course.liked_by.all():
            course.liked_by.remove(request.user)
        else:
            course.liked_by.add(request.user)
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)

class DetailCourse(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'detail_course.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = Course.objects.get(pk=self.kwargs['course_id'])
        
    
        context = super().get_context_data(**kwargs)
        rating = Rate.objects.filter(course=self.object).aggregate(Avg('rate'))['rate__avg']
        if rating:
            context['rating'] = round(rating, 2)
        else:
            context['rating'] = 0
        # context['comments'] = Comment.objects.filter(post=self.object)
        # context['comment_form'] = CommentForm()  
        context['rate_form'] = RateForm()       # Add rate form to context
        flag = Enrollment.objects.filter(user=user, course=course).exists()
        if flag:
            context['status'] = True
        else:
            context['status'] = False
        return context

    def post(self, request, *args, **kwargs):
        # comment_form = CommentForm(request.POST)
        rate_form = RateForm(request.POST)

        # if comment_form.is_valid():
        #     comment = comment_form.save(commit=False)
        #     post = self.get_object()
        #     comment.post = post
        #     comment.user = request.user
        #     comment.save()
        #     return redirect('post', post_id=post.pk)  

        if rate_form.is_valid():
            rate = rate_form.save(commit=False)
            course = self.get_object()
            rate.course = course
            rate.user = request.user 
            rate.save()
            return redirect('course', course_id= course.pk)  

        return super().post(request, *args, **kwargs) 
        
class Enroll(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        Enrollment.objects.create(user=request.user, course=course)
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    
class UpdateLesson(IsLessonOwener, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'update_lesson.html'
    pk_url_kwarg = 'lesson_id'
    success_url = reverse_lazy('home')
    
class DeleteLesson(LoginRequiredMixin, IsLessonOwener, DeleteView):
    login_url = reverse_lazy("login")
    model = Lesson
    pk_url_kwarg = 'lesson_id'
    success_url = reverse_lazy('dashboard')
    
    
class EnrolledCourses(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'dashboard.html'
    context_object_name = 'courses'
    login_url = reverse_lazy("login")
    
    def get_queryset(self):
        return Course.objects.filter(get_enrollments__user=self.request.user)
    
class Favorite(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'dashboard.html'
    context_object_name = 'courses'
    login_url = reverse_lazy("login")
    
    def get_queryset(self):
        return Course.objects.filter(liked_by=self.request.user)