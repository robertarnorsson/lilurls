from django import forms

from captcha.fields import CaptchaField, CaptchaTextInput

from shortener import models

class UrlForm(forms.Form):
    long_url = forms.CharField(
        label="Website URL",
        widget=forms.URLInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )
    captcha_field = CaptchaField(
        widget=CaptchaTextInput(attrs={'class': 'w-full py-1 px-2 text-gray-300 text-sm placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800', 'placeholder': 'Captcha'})
    )

class TrackingForm(forms.Form):
    tracking_url = forms.URLField(
        label="Shortened URL",
        widget=forms.URLInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )

class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['url', 'violation_type', 'message']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Shortened URL','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'violation_type': forms.Select(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800', 'rows': 4}),
        }
