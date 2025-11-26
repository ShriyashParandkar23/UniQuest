
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({"status": "healthy", "message": "UniQuest Backend is running!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check, name='health_check'),
    # path('', include('app.urls')),
    path('api/colleges/', include('college.urls')),

    path('api/llm/', include('chat.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
