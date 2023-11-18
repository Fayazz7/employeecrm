"""
URL configuration for employeecrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crm import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.IndexView.as_view(),name="index"),
    path('add/',views.EmployeeCreateView.as_view(),name="emp-add"),
    path('list/',views.EmployeeListView.as_view(),name="emp-list"),
    path('<int:pk>/update',views.EmployeeUpdateView.as_view(),name="emp-update"),
    path("<int:pk>",views.EmployeeDetalView.as_view(),name="emp-detail"),
    path('<int:pk>/remove',views.EmployeeDeleteView.as_view(),name="emp-delete"),
    path('signup/',views.SignUpView.as_view(),name='sign-up'),
    path('',views.SignInView.as_view(),name="sign-in"),
    path('logout',views.SignOutView.as_view(),name="sign-out")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
