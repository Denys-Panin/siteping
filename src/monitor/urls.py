from django.urls import path
from .views import MonitorSiteListCreateView, SiteCheckLogListView, SiteChartDataView, site_chart_view, site_select_view


urlpatterns = [
    path("sites/", MonitorSiteListCreateView.as_view(), name="site-list-create"),
    path("sites/<int:pk>/logs/", SiteCheckLogListView.as_view(), name="site-logs"),
    path("sites/<int:pk>/chart/", SiteChartDataView.as_view(), name="site-chart"),
]
