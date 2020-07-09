from django.conf.urls import url
from amigo import views

urlpatterns = [
    #url('hello/',views.greetings),
    url('signup',views.sign_up_page),
    url('home',views.home,name='home'),
    url('login',views.login_page,name='login_page'),
    url('logout',views.userLogout,name='userLogout'),
    url('profile',views.profile,name='profile'),
    url('about',views.about,name='about'),
    url('photos',views.photos,name='photos'),
    url('friends',views.friends,name='friends'),
    url('upload',views.upload,name='upload'),
    url('like_post',views.like_post,name='like_post'),

]
