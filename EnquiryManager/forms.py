from django import forms
from .models import Enquiry,Consultation,DynamicField

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "enquiry_date",
            "customer_name",
            "mobile_no",
            "email",
            "country",
            "state",
            "city",
            "pincode",
            "enquiry_description",
            "enquiry_for",
            "patient_type",
            "source_of_enquiry",
            "referred_by",
            "interest"
        ]
        widgets = {
            "enquiry_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full Name"
            }),
            "mobile_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Mobile Number"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email id"
            }),

            # Country — existing style
            "country": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "country-options",
                "placeholder": "Start typing a country..."
            }),

            # State — same style
            "state": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "state-options",
                "placeholder": "Start typing a state..."
            }),

            # City — same style
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "city-options",
                "placeholder": "Start typing a city..."
            }),

            # Pincode — same style
            "pincode": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "pincode-options",
                "placeholder": "Start typing a pincode..."
            }),

            "enquiry_description": forms.Textarea(attrs={
                "class": "form-control"
            }),

            "enquiry_for": forms.Select(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "interest-options",
                "placeholder": "Select"
            }),

            "patient_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "source_of_enquiry": forms.Select(attrs={
                "class": "form-control"
            }),
            "referred_by": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional"
            }),
            "interest": forms.Select(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "interest-options",
                "placeholder": "Select"
                
            }),
        }

class DynamicEnquiryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DynamicEnquiryForm, self).__init__(*args, **kwargs)

        for field in DynamicField.objects.all():
            field_name = field.name.lower().replace(" ", "_")
            if field.field_type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=field.name,
                    required=field.required,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )
            elif field.field_type == 'number':
                self.fields[field_name] = forms.IntegerField(
                    label=field.name,
                    required=field.required,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )
            elif field.field_type == 'date':
                self.fields[field_name] = forms.DateField(
                    label=field.name,
                    required=field.required,
                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
                )

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient_name', 'appointment_date', 'consultation_time', 'doctor', 'consultation_type']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'consultation_time': forms.TimeInput(attrs={'type': 'time'}),
        }
class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['appointment_date', 'consultation_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'consultation_time': forms.TimeInput(attrs={'type': 'time'})
        }
