from django import forms

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from shortener import models

class UrlForm(forms.Form):
    long_url = forms.CharField(
        label="Website URL",
        widget=forms.URLInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3(action='shorten'))

class TrackingForm(forms.Form):
    tracking_url = forms.URLField(
        label="Shortened URL",
        widget=forms.URLInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3(action='tracking'))

class ReportForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3(action='report'))

    class Meta:
        model = models.Report
        fields = ['url', 'violation_type', 'message', 'captcha']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Shortened URL','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'violation_type': forms.Select(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].required = True
