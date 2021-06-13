from django.urls import path, include

from .views import home, post_detail, registration

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('', home, name='home'),
]