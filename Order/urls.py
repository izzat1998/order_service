"""Order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.documentation import include_docs_urls

urlpatterns = [

    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:

    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('counterparty/', include('apps.counterparty.urls')),
    path('core/', include('apps.core.urls')),
    path('order/', include('apps.order.urls')),
    path('container_order/', include('apps.container_order.urls')),
    path('wagon_order/', include('apps.wagon_order.urls')),
    path('wagon_empty_order/', include('apps.wagon_empty_order.urls')),
    path('statistic/', include('apps.statistic.urls')),
    path('code/', include('apps.code.urls')),

]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
