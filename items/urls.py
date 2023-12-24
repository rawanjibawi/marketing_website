from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'item'
urlpatterns = [
    
    path('', views.items, name='search'),
    path('<int:id>/', views.detail, name='detail'),
    path('add-item', views.add_item, name='add-item'),
    path('<int:id>/delete', views.delete, name='delete'),
    path('<int:id>/edit', views.edit_item, name='edit'),
    path('add-cart', views.add_cart, name='add-cart')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
