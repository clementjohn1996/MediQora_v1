from django.db import models
from django.utils import timezone


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class PatientCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Enquiry(models.Model):
    enquiry_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()

    country = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length=50)
    enquiry_for = models.CharField(max_length=255, blank=True, null=True)

    # Patient Type Choices
    PATIENT_TYPES = [
        ('OPD', 'Outpatient'),
        ('IPD', 'Inpatient'),
        ('Emergency', 'Emergency'),
    ]
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPES)

    # Enquiry Source Choices
    ENQUIRY_SOURCES = [
        ('Website', 'Website'),
        ('Phone Call', 'Phone Call'),
        ('Walk-in', 'Walk-in'),
        ('Referral', 'Referral'),
    ]
    source_of_enquiry = models.CharField(max_length=100, choices=ENQUIRY_SOURCES)

    referred_by = models.CharField(max_length=100, blank=True, null=True)
    enquiry_description = models.TextField()

    def __str__(self):
        return self.customer_name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ConsultationType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Consultation(models.Model):
    patient_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    consultation_type = models.ForeignKey(ConsultationType, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=(("Pending", "Pending"), ("Processed", "Processed")), default="Pending"
    )

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"


class Surgery(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    surgery_type = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=(("Scheduled", "Scheduled"), ("Completed", "Completed")), default="Scheduled"
    )

    def __str__(self):
        return f"{self.patient_name} - {self.surgery_type}"
