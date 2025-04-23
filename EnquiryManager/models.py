from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO

class PatientCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class EnquiryFor(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Enquiry For"
        verbose_name_plural = "Enquiry For"

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    enquiry_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()
    qr_code_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    pincode = models.CharField(max_length=50)
    enquiry_for =  models.ForeignKey(EnquiryFor, on_delete=models.CASCADE)

    PATIENT_TYPES = [
        ('OPD', 'Outpatient'),
        ('IPD', 'Inpatient'),
        ('Emergency', 'Emergency'),
    ]
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPES)

    ENQUIRY_SOURCES = [
        ('Website', 'Website'),
        ('Phone Call', 'Phone Call'),
        ('Walk-in', 'Walk-in'),
        ('Referral', 'Referral'),
    ]
    source_of_enquiry = models.CharField(max_length=100, choices=ENQUIRY_SOURCES)
    referred_by = models.CharField(max_length=100, blank=True, null=True)

    INTEREST_CHOICES = [
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('waiting', 'Waiting for Decision'),
    ]
    interest= models.CharField(
        max_length=20,
        choices=INTEREST_CHOICES,
        default='waiting',
        verbose_name='Interest'
    )

    enquiry_description = models.TextField()

    def __str__(self):
        return self.customer_name



# ✅ For storing unique state values
class StateEntry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ For storing unique city values
class CityEntry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ For storing unique pincode values (optional, if needed)
class PincodeEntry(models.Model):
    value = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.value


# ✅ Dynamic Field Definitions
class DynamicField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('dropdown', 'Dropdown'),
    )

    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ✅ Key-Value storage for dynamic field values linked to enquiry
class EnquiryAdditionalField(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='additional_fields')
    field_name = models.CharField(max_length=255)
    field_value = models.TextField()

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ConsultationType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name
    
class SurgeryType(models.Model):
    title = models.CharField(max_length=100)
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name
    
class Consultation(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='consultations', null=True, blank=True)
    is_surgery_scheduled = models.BooleanField(default=False)
    surgery_type = models.ForeignKey(SurgeryType, on_delete=models.SET_NULL, null=True, blank=True)
    patient_name = models.CharField(max_length=255)
    appointment_date = models.DateField()
    consultation_time = models.TimeField(null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    consultation_type = models.ForeignKey(ConsultationType, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=(("Pending", "Pending"), ("Processed", "Processed")), default="Pending"
    )
    description = models.CharField(max_length=255)
    qr_code_image = models.ImageField(upload_to='consultation_qrcodes/', blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code_image:
            qr_data = f"Consultation ID: {self.id}\nPatient: {self.patient_name}\nDoctor: {self.doctor.name}"
            qr = qrcode.make(qr_data)
            stream = BytesIO()
            qr.save(stream, format='PNG')
            self.qr_code_image.save(f"consultation_{self.id}.png", ContentFile(stream.getvalue()), save=False)
            super().save(update_fields=['qr_code_image'])



class Surgery(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField()
    surgery_type = models.ForeignKey(SurgeryType, on_delete=models.CASCADE, null=True, blank=True)
    scheduled_date = models.DateField()  
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=(("Scheduled", "Scheduled"), ("Completed", "Completed")),
        default="Scheduled"
    )
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.surgery_type}"
