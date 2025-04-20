from django.core.paginator import Paginator
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.utils.timezone import localdate
from django.db import IntegrityError
from django.contrib import messages
from .models import (
    Enquiry, Doctor, Consultation, ConsultationType, Surgery,SurgeryType,
    StateEntry, CityEntry, PincodeEntry
)
from .forms import EnquiryForm, DynamicEnquiryForm, ConsultationForm
import qrcode
import io
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Enquiry, Consultation
import qrcode
from django.core.files import File
from django.core.files.base import ContentFile
from io import BytesIO
import os
from django.conf import settings
from django.urls import reverse
# ----------------- ENQUIRIES -----------------

@login_required
def enquiry_create(request):
    today = localdate()
    enquiries_today = Enquiry.objects.filter(enquiry_date=today).order_by('-id')

    paginator = Paginator(enquiries_today, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    new_id = request.GET.get("new_id")  # Get newly created enquiry id if passed

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)

            # Generate QR data
            qr_data = (
                f"Mob: {enquiry.mobile_no}\n"
                f"Name: {enquiry.customer_name}\n"
                f"Enquiry For: {enquiry.enquiry_for}\n"
                f"Enquiry Description: {enquiry.enquiry_description}"
            )
            qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()

            # Check for duplicates
            if Enquiry.objects.filter(qr_code_hash=qr_hash).exists():
                messages.error(request, "This enquiry already exists.")
                return redirect('enquiry_create')

            enquiry.qr_code_hash = qr_hash

            # Generate QR code image
            qr_image = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            buffer.seek(0)

            # Ensure qr_codes directory exists
            qr_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            os.makedirs(qr_folder, exist_ok=True)

            filename = f'{qr_hash}.png'
            enquiry.qr_code_image.save(filename, File(buffer), save=False)

            enquiry.save()

            # Redirect with new enquiry id
            return redirect(f"{reverse('enquiry_create')}?new_id={enquiry.id}")
    else:
        form = EnquiryForm()

    return render(request, 'EnquiryManager/enquiry_create.html', {
        'form': form,
        'enquiries_today': enquiries_today,
        'page_obj': page_obj,
        'new_id': new_id,
    })


@login_required
def enquiry_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        enquiries = Enquiry.objects.filter(
            customer_name__icontains=search_query
        ).order_by('-enquiry_date')
    else:
        today = localdate()
        enquiries = Enquiry.objects.filter(enquiry_date=today).order_by('-created_at')

    paginator = Paginator(enquiries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'EnquiryManager/enquiry_list.html', {
        'enquiries': page_obj,
        'search_query': search_query
    })

def save_unique(model, value):
    if value:
        field_name = 'name' if hasattr(model, 'name') else 'value'
        if not model.objects.filter(**{field_name: value}).exists():
            try:
                model.objects.create(**{field_name: value})
            except IntegrityError:
                pass

def pending_enquiries(request):
    # Only enquiries still marked interested/waiting AND without any consultation yet:
    pending_list = (
        Enquiry.objects
               .filter(interest__in=['interested', 'waiting'])
               .filter(consultations__isnull=True)
               .order_by('-enquiry_date')
    )
    return render(request, 'EnquiryManager/pending_enquiries.html', {
        'pending_list': pending_list
    })

@login_required
def enquiry_edit(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    if request.method == "POST":
        form = EnquiryForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            return redirect('enquiry_list')
    else:
        form = EnquiryForm(instance=enquiry)
    return render(request, 'EnquiryManager/enquiry_form.html', {'form': form})

@login_required
def enquiry_delete(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    enquiry.delete()
    return redirect('enquiry_list')

def state_autocomplete(request):
    term = request.GET.get('term', '')
    states = StateEntry.objects.filter(name__icontains=term).order_by('name').values_list('name', flat=True).distinct()
    return JsonResponse(list(states), safe=False)

def city_autocomplete(request):
    term = request.GET.get('term', '')
    cities = CityEntry.objects.filter(name__icontains=term).order_by('name').values_list('name', flat=True).distinct()
    return JsonResponse(list(cities), safe=False)

@csrf_exempt
def save_state_city(request):
    if request.method == "POST":
        state_name = request.POST.get("state", "").strip().title()
        city_name = request.POST.get("city", "").strip().title()

        if state_name:
            state, _ = StateEntry.objects.get_or_create(name=state_name)
            if city_name:
                CityEntry.objects.get_or_create(name=city_name, state=state)

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

def pincode_autocomplete(request):
    term = request.GET.get('term', '')
    pincodes = Enquiry.objects.filter(pincode__icontains=term).values_list('pincode', flat=True).distinct()
    return JsonResponse(list(pincodes), safe=False)

def enquiry_for_autocomplete(request):
    term = request.GET.get("term", "")
    results = Enquiry.objects.filter(enquiry_for__icontains=term) \
        .values_list("enquiry_for", flat=True).distinct().order_by("enquiry_for")
    return JsonResponse(list(results), safe=False)

# ----------------- CONSULTATIONS -----------------

@login_required
def consultation(request):
    today = localdate()

    # Exclude consultations with surgery already scheduled
    consultations_today = Consultation.objects.filter(
        appointment_date=today,
        is_surgery_scheduled=False
    ).order_by('appointment_date')

    upcoming_consultations = Consultation.objects.filter(
        appointment_date__gt=today,
        is_surgery_scheduled=False
    ).order_by('appointment_date')

    expired_consultations = Consultation.objects.filter(
        appointment_date__lt=today,
        is_surgery_scheduled=False
    ).order_by('appointment_date')

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultation')
    else:
        form = ConsultationForm()

    context = {
        'todays': consultations_today,
        'upcoming': upcoming_consultations,
        'expired': expired_consultations,
        'form': form,
        'today': today,
    }

    return render(request, 'consultations/consultation.html', context)

@login_required
def complete_consultation(request, enquiry_id):
    consultation = get_object_or_404(Consultation, id=enquiry_id)
    consultation.status = 'Completed'
    consultation.save()
    return redirect('consultation')

@login_required
def reschedule(request, enquiry_id):
    today = date.today()
    
    # Try to get the entity from both Consultation and Surgery models
    consultation = Consultation.objects.filter(id=enquiry_id).first()
    surgery = Surgery.objects.filter(id=enquiry_id).first()
    
    # Determine the entity based on which model the enquiry_id belongs to
    if consultation:
        entity_type = 'consultation'
        entity = consultation
    elif surgery:
        entity_type = 'surgery'
        entity = surgery
    else:
        return redirect('surgeries')  # or another default page if no such entity
    
    if request.method == 'POST':
        # Handle the form submission and update the scheduled date
        new_date = request.POST.get('scheduled_date')
        entity.scheduled_date = new_date
        entity.save()
        return redirect('consultations') if entity_type == 'consultation' else redirect('surgeries')

    # Render the reschedule form with the current date
    return render(request, 'reschedule.html', {
        'entity': entity,
        'entity_type': entity_type,
        'today': today
    })

@login_required
def add_consultation(request):
    doctors = Doctor.objects.all()
    types = ConsultationType.objects.all()

    # Use appointment_date everywhere, not consultation_date
    consultations = Consultation.objects.filter(
        appointment_date__gte=date.today()
    ).order_by('appointment_date')

    # Filtering by doctor, patient, or date
    doctor_filter  = request.GET.get('doctor')
    patient_filter = request.GET.get('patient')
    date_filter    = request.GET.get('appointment_date')

    if doctor_filter:
        consultations = consultations.filter(doctor_id=doctor_filter)
    if patient_filter:
        consultations = consultations.filter(patient_name__icontains=patient_filter)
    if date_filter:
        consultations = consultations.filter(appointment_date=date_filter)

    return render(request, 'consultations/add_consultation.html', {
        'consultations': consultations,
        'doctors': doctors,
        'types': types,
    })


@login_required
def edit_consultation(request, enquiry_id):
    consultation = get_object_or_404(Consultation, id=enquiry_id)

    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect('consultation_detail', enquiry_id=consultation.id)
    else:
        form = ConsultationForm(instance=consultation)

    return render(request, 'edit_consultation.html', {'form': form, 'consultation': consultation})
@login_required
def mark_as_processed(request, id):
    consultation = get_object_or_404(Consultation, id=id)
    consultation.status = "Processed"
    consultation.save()
    return redirect('consultation')

@login_required
def add_consultation_from_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    doctors = Doctor.objects.all()
    types = ConsultationType.objects.all()

    initial_data = {
        'patient_name': enquiry.customer_name,
        'description': enquiry.enquiry_description,
        'mobile_no': enquiry.mobile_no,
        'enquiry_for': enquiry.enquiry_for,
    }

    if request.method == 'POST':
        # Getting submitted values
        patient_name = request.POST.get('patient_name', enquiry.customer_name)
        description = request.POST.get('description', enquiry.enquiry_description)
        doctor_id = request.POST.get('doctor')
        consultation_type_id = request.POST.get('consultation_type')
        appointment_date = request.POST.get('appointment_date')

        if not appointment_date or not doctor_id or not consultation_type_id:
            # You can add a proper validation message here
            return redirect('add_consultation_from_enquiry', enquiry_id=enquiry.id)

        doctor = get_object_or_404(Doctor, id=doctor_id)
        consult_type = get_object_or_404(ConsultationType, id=consultation_type_id)

        # Create consultation
        consultation = Consultation.objects.create(
            enquiry=enquiry,
            patient_name=patient_name,
            description=description,
            doctor=doctor,
            consultation_type=consult_type,
            appointment_date=appointment_date,
            status="Processed",
        )

        # ✅ Regenerate QR code with updated description
        qr_data = (
            f"Mob: {enquiry.mobile_no}\n"
            f"Name: {enquiry.customer_name}\n"
            f"Enquiry For: {enquiry.enquiry_for}\n"
            f"Enquiry Description: {description}"
        )
        qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()
        enquiry.qr_code_hash = qr_hash

        # Generate QR code
        qr_image = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Save QR image to MEDIA folder
        qr_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_folder, exist_ok=True)
        filename = f"{qr_hash}.png"
        enquiry.qr_code_image.save(filename, File(buffer), save=False)

        # Update description and save enquiry
        enquiry.enquiry_description = description
        enquiry.save()

        return redirect('consultation')

    return render(request, 'consultations/add_consultation.html', {
        'enquiry': enquiry,
        'doctors': doctors,
        'types': types,
        'initial_data': initial_data,
    })

# ----------------- SURGERIES -----------------
@login_required
def schedule_surgery(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    doctors = Doctor.objects.all()
    types = SurgeryType.objects.all()

    # Fetch the most recent consultation for the enquiry
    consultation = Consultation.objects.filter(enquiry=enquiry).last()

    if request.method == 'POST':
        patient = request.POST.get('patient_name')
        desc = request.POST.get('description')
        doctor_id = request.POST.get('doctor')
        surgery_type_id = request.POST.get('surgery_type')
        appt_date = request.POST.get('surgery_date')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        surgery_type = get_object_or_404(SurgeryType, id=surgery_type_id)

        # Create the surgery record
        surgery = Surgery.objects.create(
            patient_name=patient,
            description=desc,
            doctor=doctor,
            surgery_type=surgery_type,
            scheduled_date=appt_date,
            status='Scheduled',
            enquiry=enquiry  # Optional: link it if your model supports this
        )

        # Update consultation status if available
        if consultation:
            consultation.is_surgery_scheduled = True
            consultation.save()

        # Generate QR Code
        qr_data = f"Surgery for: {surgery.patient_name}\nDoctor: {doctor.name}\nType: {surgery.surgery_type.title}\nDate: {surgery.scheduled_date}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the QR code to the Surgery model (assuming you have a field to store it)
        surgery.qr_code.save(f"qr_code_{surgery.id}.png", ContentFile(buffer.read()), save=True)

        # Redirect to the surgeries page after saving the surgery
        return redirect('surgeries')  # Assuming 'surgeries' is the name of your surgeries list view

    # Pre-fill data from consultation if available
    initial_data = {
        'patient_name': enquiry.customer_name,
        'description': consultation.description if consultation else '',
        'doctor': consultation.doctor.id if consultation and consultation.doctor else '',
    }

    surgeries = Surgery.objects.filter(scheduled_date__gte=date.today()).order_by('scheduled_date')
    return render(request, 'surgeries/add_surgery.html', {
        'doctors': doctors,
        'types': types,
        'surgeries': surgeries,
        'enquiry': enquiry,
        'consultation': consultation,  # 👈 pass the consultation directly
    })

@login_required
def surgeries(request):
    doctors = Doctor.objects.all()
    types = SurgeryType.objects.all()
    today = localdate()

    pending = Surgery.objects.filter(status="Scheduled", scheduled_date=today)
    upcoming = Surgery.objects.filter(status="Scheduled", scheduled_date__gt=today)
    processed = Surgery.objects.filter(status="Completed")

    if request.method == 'POST':
        patient = request.POST.get('patient_name')
        desc = request.POST.get('description')
        doctor_id = request.POST.get('doctor')
        surgery_type_id = request.POST.get('surgery_type')
        scheduled_date = request.POST.get('scheduled_date')

        # Validate required fields
        if patient and desc and doctor_id and surgery_type_id and scheduled_date:
            doctor = get_object_or_404(Doctor, id=doctor_id)
            surgery_type_obj = get_object_or_404(SurgeryType, id=surgery_type_id)

            Surgery.objects.create(
                patient_name=patient,
                description=desc,
                doctor=doctor,
                surgery_type=surgery_type_obj,
                scheduled_date=scheduled_date,
                status="Scheduled"
            )
            return redirect('surgeries')
        else:
            # Optionally: add error message here using messages framework
            pass  # Still fall through to render the page below

    # Make sure this always returns a response
    return render(request, 'surgeries/surgeries.html', {
        'doctors': doctors,
        'types': types,
        'pending': pending,
        'upcoming': upcoming,
        'processed': processed
    })


def generate_qr_code(surgery):
    # Create the QR code for the surgery
    qr_data = f"Surgery scheduled for {surgery.patient_name} on {surgery.scheduled_date}"
    qr_img = qrcode.make(qr_data)

    # Save the QR code as an image in a BytesIO object
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Save the image to the Surgery model's field (qr_code)
    surgery.qr_code.save(f"qr_code_{surgery.id}.png", ContentFile(img_io.read()), save=True)

    return surgery.qr_code



def feedback(request):
    feedback=[]
    return render(request, 'feedback', {'feedback': feedback})