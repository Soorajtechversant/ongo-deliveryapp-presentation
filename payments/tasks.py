from datetime import timedelta, datetime

from projectfolderongo.celery import app
from ongoappfolder.models import MerchantDetails
from payments.models import Report
from projectfolderongo import settings as django_settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Sum







@app.task(name='send_daily_report')
def send_weekly_reports():

    date = datetime.now()
    merchants = MerchantDetails.objects.all()
    for merchant in merchants:
        reports = Report.objects.filter(hotel=merchant, purchase_date=date)
        total_profit = reports.aggregate(Sum('amount'))['amount__sum']
        print(total_profit)
        if reports:
            ctx = {}
            ctx['merchant'] = merchant
            ctx['reports'] = reports
            ctx['profit'] = total_profit
            print(ctx)
            try:
                template = 'products/productshop_owner/report_mail.html'

                html_message = render_to_string(template, ctx)
                message = strip_tags(html_message)
                subject = 'Daily Report'
                from_email = django_settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [merchant.email], html_message=html_message)
            except Exception as e:
                print(str(e))
                pass
        else:
            print('No reports for', merchant)



