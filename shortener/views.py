from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render

import random
import string
import datetime
import requests
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

def is_lilurls_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith('lilurls.com')

def is_website_up(url):
    try:
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            return True
        elif response.is_redirect or response.is_permanent_redirect:
            return False
        else:
            return False
    except requests.RequestException:
        return False

def shortener(request):
    counter = models.UrlCounter.objects.first()
    count = counter.count if counter else 0

    if request.method == "POST":
        form = forms.UrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['long_url']

            if is_lilurls_domain(original_url):
                messages.error(request, "You cannot shorten a URL that is already from lilurls.com.")
                return render(request, 'home.html', {'form': form, 'total_count': count})

            if not is_website_up(original_url):
                messages.error(request, "There seems to not be any website for that URL or it is a redirect. Please try again if you think this is a mistake.")
                return render(request, 'home.html', {'form': form, 'total_count': count})

            url_trail = generate_random_url()
            expiration_period = datetime.timedelta(days=7)
            expiration_date = datetime.datetime.now() + expiration_period
            short_url = models.UrlModel(
                original_url=original_url, 
                short_url_extension=url_trail, 
                expiration_date=expiration_date
            )
            short_url.save()

            counter, _ = models.UrlCounter.objects.get_or_create(id=1)
            counter.increment()

            full_short_url = request.build_absolute_uri('/u/') + url_trail
            count = counter.count if counter else 0
            return render(request, 'home.html', {'form': form,'short_url': full_short_url, 'total_count': count})
        else:
            messages.error(request, "Captcha is not valid")
    
    counter = models.UrlCounter.objects.first()
    count = counter.count if counter else 0
    form = forms.UrlForm()
    return render(request, 'home.html', {'form': form, 'total_count': count})

def tracking(request):
    if request.method == "POST":
        form = forms.TrackingForm(request.POST)
        if form.is_valid():
            tracking_url = form.cleaned_data['tracking_url']

            if not is_lilurls_domain(tracking_url):
                messages.error(request, "You can only track URLs from lilurls.com.")
                return render(request, 'tracking.html', {'form': form})

            url_trail = get_url_trail(tracking_url)
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
    try:
        url = models.UrlModel.objects.get(short_url_extension=short_url_extension)
        total_reports = url.get_reports()

        if url.is_expired():
            url.delete()
            messages.error(request, "This URL has expired.")
            return redirect('shortener')

        if total_reports >= 10:
            url.delete()
            messages.error(request, "This URL has been removed due to reports.")
            return redirect('shortener')

        if total_reports >= 2:
            full_warning_url = request.build_absolute_uri('/w/') + short_url_extension
            return redirect(full_warning_url)

        url.increment()
        return redirect(url.original_url)

    except models.UrlModel.DoesNotExist:
        messages.error(request, "The requested URL does not exist.")
        return redirect('shortener')

def track_url(request, short_url_extension):
    try:
        url = models.UrlModel.objects.get(short_url_extension=short_url_extension)
        original_url = url.get_original()
        count = url.get_counter()
        days_left = url.get_days_left()
        total_reports = url.get_reports()

        if url.is_expired():
            url.delete()
            messages.error(request, "This URL has expired.")
            return redirect('shortener')

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

    except models.UrlModel.DoesNotExist:
        messages.error(request, "The requested URL does not exist.")
        return redirect('shortener')

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

def redirect_warning(request, short_url_extension):
    try:
        url_model = models.UrlModel.objects.get(short_url_extension=short_url_extension)
        original_url = url_model.get_original()
        total_reports = url_model.get_reports()
        full_short_url = request.build_absolute_uri('/u/') + short_url_extension

        return render(request, 'redirect_warning.html', {
            'total_reports': total_reports,
            'original_url': original_url,
            'short_url': full_short_url
        })

    except models.UrlModel.DoesNotExist:
        messages.error(request, "The requested URL does not exist.")
        return redirect('shortener')

def error_404(request, _):
    messages.error(request, "That URL does not exist or has expired!")
    return redirect('shortener')

def error_500(request):
    messages.error(request, "An error happened on our servers!")
    return redirect('shortener')