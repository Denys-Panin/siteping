import requests
import time
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import MonitoredSite, SiteCheckLog


@shared_task
def check_site():
    sites = MonitoredSite.objects.all()

    for site in sites:
        alert_message = ""
        alert = False

        try:
            start = time.time()
            response = requests.get(site.url, timeout=5)
            end = time.time()
            response_time = round(end - start, 2)

            SiteCheckLog.objects.create(
                site=site,
                status_code=response.status_code,
                response_time=response_time,
                is_online=response.ok
            )

            if not response.ok:
                alert = True
                alert_message = f"{site.name} ({site.url}) returned status {response.status_code}."

            elif response_time > 1.5:
                alert = True
                alert_message = f"{site.name} ({site.url}) answers slowly: {response_time} sec."

        except Exception as e:
            SiteCheckLog.objects.create(
                site=site,
                status_code=0,
                response_time=0,
                is_online=False
            )
            alert = True
            alert_message = f"{site.name} ({site.url}) inaccessible: {str(e)}"

        if alert:
            send_mail(
                subject="⚠️ Problem with site monitoring",
                message=f"There was a problem.:\n\n{alert_message}",
                from_email=None,
                recipient_list=[site.user.email],
                fail_silently=True
            )
