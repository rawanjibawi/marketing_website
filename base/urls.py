from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from .forms import LoginForm
urlpatterns = [
    path('browse/', views.show_all, name='browse'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # path('login/', auth_view.LoginView.as_view(template_name='login.html',
        #  authentication_form=LoginForm), name='login'),
    # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

