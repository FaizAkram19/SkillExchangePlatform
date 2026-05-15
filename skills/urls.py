from skills import views
from django.urls import path

urlpatterns=[
    path("userskills/", views.UserSkills.as_view()),
    path("userskills/<int:pk>/", views.SkillDetail.as_view()),
    path("skills/",views.SkillList.as_view()),
    path("skills/create/", views.CreateSkill.as_view())
]