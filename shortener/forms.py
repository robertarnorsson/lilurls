from django import forms
from .models import Report

class UrlForm(forms.Form):
    long_url = forms.CharField(
        label="Website URL",
        widget=forms.TextInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )

class TrackingForm(forms.Form):
    tracking_url = forms.URLField(
        label="Shortened URL",
        widget=forms.URLInput(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded-l border-2 border-transparent focus:outline-none focus:border-neutral-800'})
    )

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['url', 'violation_type', 'message']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Shortened URL','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'violation_type': forms.Select(attrs={'class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message','class': 'w-full py-3 px-4 text-gray-300 placeholder-dark-600 bg-dark-900 rounded border-2 border-transparent focus:outline-none focus:border-neutral-800', 'rows': 4}),
        }
