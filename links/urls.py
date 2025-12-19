from django.urls import path , include


urlpatterns = [
    path('api/v1/', include('links.api.v1.urls'))
]