from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from .models import MonitoredSite, SiteCheckLog
from .serializers import (
    MonitoredSiteSerializer,
    SiteCheckLogSerializer,
    SiteCheckChartSerializer
)


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="admin").exists()


class MonitorSiteListCreateView(generics.ListCreateAPIView):
    serializer_class = MonitoredSiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if is_admin(self.request.user):
            return MonitoredSite.objects.all()
        return MonitoredSite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SiteCheckLogListView(generics.ListAPIView):
    serializer_class = SiteCheckLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        site_id = self.kwargs['pk']
        if is_admin(self.request.user):
            site = get_object_or_404(MonitoredSite, pk=site_id)
        else:
            site = get_object_or_404(MonitoredSite, pk=site_id, user=self.request.user)

        return SiteCheckLog.objects.filter(site=site).order_by('-checked_at')


class SiteChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if is_admin(request.user):
            site = get_object_or_404(MonitoredSite, pk=pk)
        else:
            site = get_object_or_404(MonitoredSite, pk=pk, user=request.user)

        logs = SiteCheckLog.objects.filter(site=site).order_by('checked_at')
        serializer = SiteCheckChartSerializer(logs, many=True)
        return Response(serializer.data)


@login_required
def site_chart_view(request, pk):
    if is_admin(request.user):
        site = get_object_or_404(MonitoredSite, pk=pk)
    else:
        site = get_object_or_404(MonitoredSite, pk=pk, user=request.user)

    token = AccessToken.for_user(request.user)

    return render(request, "monitor/chart.html", {
        "site_id": site.id,
        "site_name": site.name,
        "site_url": site.url,
        "token": str(token)
    })


@login_required
def site_select_view(request):
    if is_admin(request.user):
        sites = MonitoredSite.objects.all()
    else:
        sites = MonitoredSite.objects.filter(user=request.user)

    return render(request, "monitor/select_site.html", {"sites": sites})
