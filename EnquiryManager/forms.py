from django import forms
from .models import Enquiry

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

            "enquiry_for": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "list": "enquiry-options",  # Must match <datalist id="">
                "placeholder": "Enquiry for..."
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
        }
