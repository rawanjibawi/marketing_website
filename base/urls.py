from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path
from django.contrib.auth import views as auth_view # use it for reset password
from . import views

urlpatterns = [
    path('browse/', views.show_all, name='browse'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset-password/', auth_view.PasswordResetView.as_view(template_name='reset_password.html'),  name="reset_password"),
    path('reset-password-send/', auth_view.PasswordResetDoneView.as_view(template_name='reset_password_send.html'),  name="password_reset_done"),
    path('reset-password/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='reset_password_confirm.html'), name="password_reset_confirm"),
    path('reset-password-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name="password_reset_complete"),


    # path('login/', auth_view.LoginView.as_view(template_name='login.html',
        #  authentication_form=LoginForm), name='login'),
    # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

