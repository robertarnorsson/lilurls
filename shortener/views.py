from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render

import random
import string
import datetime
from urllib.parse import urlparse, unquote

from shortener import forms
from shortener import models

def generate_random_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_url_trail(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    return unquote(path_parts[-1])

def check_url_exists(url_trail):
    try:
        _ = models.UrlModel.objects.get(short_url_extension=url_trail)
        return True
    except models.UrlModel.DoesNotExist:
        return False

def shortener(request):
    if request.method == "POST":
        form = forms.UrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['long_url']
            url_trail = generate_random_url()
            expiration_period = datetime.timedelta(days=7)
            expiration_date = datetime.datetime.now() + expiration_period
            short_url = models.UrlModel(original_url=original_url, short_url_extension=url_trail, expiration_date=expiration_date)
            short_url.save()

            counter, _ = models.UrlCounter.objects.get_or_create(id=1)
            counter.increment()

            full_short_url = request.build_absolute_uri('/u/') + url_trail
            count = counter.count if counter else 0
            return render(request, 'home.html', {'short_url': full_short_url, 'total_count': count})
        else:
            print("Form not valid")
            messages.error(request, "Form Not valid")
    else:
        counter = models.UrlCounter.objects.first()
        count = counter.count if counter else 0
        form = forms.UrlForm()
    return render(request, 'home.html', {'form': form, 'total_count': count})

def tracking(request):
    if request.method == "POST":
        form = forms.TrackingForm(request.POST)
        if form.is_valid():
            url_trail = get_url_trail(form.cleaned_data['tracking_url'])
            if check_url_exists(url_trail):
                full_tracking_url = request.build_absolute_uri('/t/') + url_trail
                return redirect(full_tracking_url)
            else:
                messages.error(request, "URL not found or is not valid.")
        else:
            messages.error(request, "Form not valid")
            
    form = forms.TrackingForm()
    url_trail = generate_random_url()
    example_url = request.build_absolute_uri('/u/') + url_trail
    return render(request, 'tracking.html', {'form': form, 'example_site_url': example_url})

def redirect_url(request, short_url_extension):
    url = get_object_or_404(models.UrlModel, short_url_extension=short_url_extension)
    total_reports = url.get_reports()
    if url.is_expired():
        url.delete()
        return render(request, 'home.html', status=404)
    if total_reports >= 15:
        url.delete()
        return render(request, 'home.html', status=404)
    if total_reports >= 5:
        full_warning_url = request.build_absolute_uri('/w/') + short_url_extension
        return redirect(full_warning_url)
    url.increment()
    return redirect(url.original_url)

def track_url(request, short_url_extension):
    url = get_object_or_404(models.UrlModel, short_url_extension=short_url_extension)
    original_url = url.get_original()
    count = url.get_counter()
    days_left = url.get_days_left()
    total_reports = url.get_reports()
    if url.is_expired():
        url.delete()
        return render(request, 'home.html', status=404)
    full_short_url = request.build_absolute_uri('/u/') + short_url_extension
    context = {
        'short_url': full_short_url,
        'original_url': original_url,
        'url_extension': short_url_extension,
        'total_count': count,
        'days_left': days_left,
        'total_reports': total_reports,
    }
    return render(request, 'track_url.html', context)

def report_url(request):
    form_submitted = False
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        if form.is_valid():
            short_url = form.cleaned_data['url']
            violation_type = form.cleaned_data['violation_type']
            message = form.cleaned_data['message']
            url_trail = get_url_trail(short_url)
            try:
                url_model = models.UrlModel.objects.get(short_url_extension=url_trail)
                url_model.increment_report()
                report = models.Report(url=short_url, violation_type=violation_type, message=message)
                report.save()
                form_submitted = True
            except models.UrlModel.DoesNotExist:
                messages.error(request, "The short URL does not exist in our database.")
    else:
        form = forms.ReportForm()

    return render(request, 'report.html', {'form': form, 'form_submitted': form_submitted})

def rediect_warning(request, short_url_extension):
    short_url_extension = short_url_extension
    url_model = models.UrlModel.objects.get(short_url_extension=short_url_extension)
    original_url = url_model.get_original()
    total_reports = url_model.get_reports()
    full_short_url = request.build_absolute_uri('/u/') + short_url_extension
    return render(request, 'redirect_warning.html', {'total_reports': total_reports, 'original_url': original_url, 'short_url': full_short_url})

def error_404(request, _):
    messages.error(request, "That URL does not exist or has expired!")
    return redirect(request.build_absolute_uri())

def error_500(request):
    messages.error(request, "An error happened on our servers!")
    return redirect(request.build_absolute_uri())