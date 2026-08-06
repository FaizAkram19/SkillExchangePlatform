from accounts import views
from django.urls import path

urlpatterns=[
    path("users/",views.createUser.as_view()),
    path("user/profile/", views.userProfile.as_view()),
    path("user/change-password/",views.changePassword.as_view())
]