from connections import views
from django.urls import path
app_name="connections"

urlpatterns=[
    path("connections/", views.ListConnections.as_view()),
    path("connections/request/", views.SendRequest.as_view(), name="sentreq"),
    path("connections/pending/", views.PendingConnections.as_view()),
    path("connections/pending/<int:pk>/", views.PendingDetail.as_view()),
    path("connections/<int:pk>/respond/", views.ResponseView.as_view()),
    path("connections/sent/", views.SentRequests.as_view()),
    path("connections/suggestions/", views.MatchingAlgo.as_view())
]