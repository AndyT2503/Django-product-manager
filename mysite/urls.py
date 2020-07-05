
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Shop.views import login_view



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('Shop.urls', namespace='Shop')),
    url(r'^/?$', login_view, name='login'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$',auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^password/reset/$',
                auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
                name='password_reset'),
   url(r'^password/reset/done/$',
                auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'),
                name='password_reset_done'),
   url(r'^password/reset/complete/$',
                auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'),
                name='password_reset_complete'),
   url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'),
                name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
