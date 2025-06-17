from rest_framework import serializers
from .models import MonitoredSite, SiteCheckLog


class MonitoredSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoredSite
        fields = ['id', 'name', 'url', 'check_interval', 'created_at']


class SiteCheckLogSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="site.name", read_only=True)

    class Meta:
        model = SiteCheckLog
        fields = ['checked_at', 'status_code', 'response_time', 'is_online', 'site_name']


class SiteCheckChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteCheckLog
        fields = ['checked_at', 'response_time', 'is_online']
