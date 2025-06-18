from django.contrib import admin
from django.urls import include, path
from account.views import login_view
from monitor.views import site_chart_view, site_select_view

urlpatterns = [
    path('', login_view, name="home"),
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('api/auth/', include("api.urls")),
    path('api/monitor/', include("monitor.urls")),
    path('sites/<int:pk>/chart-view/', site_chart_view, name="site-chart-view"),
    path('site/select/', site_select_view, name="site-select"),
]
