from django import forms
from .models import CitizenReport

class CitizenReportForm(forms.ModelForm):
    latitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'})
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'})
    )

    class Meta:
        model = CitizenReport
        fields = ['description', 'incident_type', 'reporter_email', 'attachments']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the incident in detail...',
                'rows': 4
            }),
            'incident_type': forms.Select(attrs={'class': 'form-control'}),
            'reporter_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email (optional)'
            }),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Incident Description',
            'incident_type': 'Type of Incident',
            'reporter_email': 'Your Email',
            'attachments': 'Attach Photos/Videos',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')
        if lat is not None and lon is not None:
            instance.location = {'lat': lat, 'lon': lon}  # save location as JSON
        if commit:
            instance.save()
        return instance
