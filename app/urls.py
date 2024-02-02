from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('signup/', SignUpWithVerification.as_view(), name='signup'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='activate'),
    path('verification_success/', VerificationSuccessView.as_view(), name='verification_success'),
    path('verification_error/', VerificationErrorView.as_view(), name='verification_error'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('creator/', BecomeCreator.as_view(), name='creator'),
    path('create/', CreateCourse.as_view(), name='create'),
    path('<int:course_id>/create_lesson/', CreateLesson.as_view(), name='create_lesson'),
    path('my_courses/', MyCourses.as_view(), name='my_courses'),
    path('delete/<int:course_id>/', DeleteCourse.as_view(), name='delete_course'),
    path('delete_lesson/<int:lesson_id>/', DeleteLesson.as_view(), name='delete_lesson'),
    path('update_course/<int:course_id>/', UpdateCourse.as_view(), name='update_course'),
    path('update_course/<int:course_id>/<int:lesson_id>', UpdateLesson.as_view(), name='update_lesson'),
    path('like/<int:course_id>', SetLike.as_view(), name='like'),
    path('course/<int:course_id>', DetailCourse.as_view(), name='course'),
    path('enroll/<int:course_id>', Enroll.as_view(), name='enroll'),
    path('enrolled/', EnrolledCourses.as_view(), name='enrolled'),
    path('favorite/', Favorite.as_view(), name='favorite'),
]