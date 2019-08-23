from django.conf.urls import url
from . import views

app_name = 'triv_tracker_app'

urlpatterns = [
    url('^$', views.index, name="index"),
    url('^login/', views.user_login, name="login"),
    url('^register/', views.register, name="register"),
    url('^logout/', views.user_logout, name="logout"),
    url('^achievements/', views.achievements, name="achievements"),
    url('^progress/', views.progress, name="progress"),
    url('^leaderboards/', views.leaderboards, name="leaderboards"),
    url('^leaderboards-all/', views.leaderboards_all, name="leaderboards_all"),
    url('^my-account/', views.my_account, name="my_account"),
    url('^contact-us/', views.contact_us, name="contact_us"),
    url('^update/', views.update, name="update"),
    url('^enter-code/', views.enter_code, name="enter_code"),
]
