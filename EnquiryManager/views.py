from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Enquiry, Consultation, Doctor, ConsultationType,Surgery
from .forms import EnquiryForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import State, City
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date
from django.utils import timezone


@login_required
def consultation(request):
    doctors = Doctor.objects.all()
    types = ConsultationType.objects.all()
    today = date.today()

    pending = Consultation.objects.filter(status="Pending", appointment_date=today)
    processed = Consultation.objects.filter(status="Processed")

    if request.method == 'POST':
        patient = request.POST.get('patient_name')
        desc = request.POST.get('description')
        doctor_id = request.POST.get('doctor')
        consult_type_id = request.POST.get('consultation_type')
        appt_date = request.POST.get('appointment_date')

        doctor = Doctor.objects.get(id=doctor_id)
        consult_type = ConsultationType.objects.get(id=consult_type_id)

        Consultation.objects.create(
            patient_name=patient,
            description=desc,
            doctor=doctor,
            consultation_type=consult_type,
            appointment_date=appt_date
        )
        return redirect('consultation')

    return render(request, 'EnquiryManager/consultation.html', {
        'doctors': doctors,
        'types': types,
        'pending': pending,
        'processed': processed
    })

def mark_as_processed(request, id):
    consultation = Consultation.objects.get(id=id)
    consultation.status = "Processed"
    consultation.save()
    return redirect('consultation')
def add_consultations(request):
    doctors = Doctor.objects.all()
    types = ConsultationType.objects.all()
    consultations = Consultation.objects.filter(appointment_date__gte=date.today()).order_by('appointment_date')
    

    doctor_filter = request.GET.get('doctor')
    patient_filter = request.GET.get('patient')
    date_filter = request.GET.get('appointment_date')

    if doctor_filter:
        consultations = consultations.filter(doctor_id=doctor_filter)
    if patient_filter:
        consultations = consultations.filter(patient_name__icontains=patient_filter)
    if date_filter:
        consultations = consultations.filter(appointment_date=date_filter)

    return render(request, 'EnquiryManager/add_consultation.html', {
        'consultations': consultations,
        'doctors': doctors,
        'types' : types,
    })


def edit_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    doctors = Doctor.objects.all()
    types = ConsultationType.objects.all()

    if request.method == 'POST':
        consultation.patient_name = request.POST.get('patient_name')
        consultation.description = request.POST.get('description')
        consultation.doctor_id = request.POST.get('doctor')
        consultation.consultation_type_id = request.POST.get('consultation_type')
        consultation.appointment_date = request.POST.get('appointment_date')
        consultation.status = request.POST.get('status')
        consultation.save()
        return redirect('upcoming_consultations')

    return render(request, 'EnquiryManager/edit_consultation.html', {
        'consultation': consultation,
        'doctors': doctors,
        'types': types,
    })    
@login_required
def surgery_schedule(request):
    surgeries = Surgery.objects.all().order_by('-scheduled_date')
    return render(request, 'EnquiryManager/schedule.html', {'surgeries': surgeries})
def add_surgery(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        patient = request.POST.get('patient_name')
        doctor_id = request.POST.get('doctor')
        surgery_type = request.POST.get('surgery_type')
        date = request.POST.get('scheduled_date')
        notes = request.POST.get('notes', '')

        doctor = get_object_or_404(Doctor, id=doctor_id)

        Surgery.objects.create(
            patient_name=patient,
            doctor=doctor,
            surgery_type=surgery_type,
            scheduled_date=date,
            notes=notes
        )
        return redirect('add_surgery')

    surgeries = Surgery.objects.all().order_by('-scheduled_date')
    return render(request, 'EnquiryManager/add_surgery.html', {
        'doctors': doctors,
        'surgeries': surgeries
    })

def today_surgeries(request):
    today = timezone.now().date()
    surgeries = Surgery.objects.filter(scheduled_date=today)
    return render(request, 'EnquiryManager/today_surgeries.html', {
        'surgeries': surgeries,
        'today': today
    })

def upcoming_surgeries(request):
    surgeries = Surgery.objects.all()

    # Filters
    doctor_id = request.GET.get('doctor')
    patient_name = request.GET.get('patient_name')
    date = request.GET.get('scheduled_date')

    if doctor_id:
        surgeries = surgeries.filter(doctor_id=doctor_id)
    if patient_name:
        surgeries = surgeries.filter(patient_name__icontains=patient_name)
    if date:
        surgeries = surgeries.filter(scheduled_date=date)

    doctors = Doctor.objects.all()

    return render(request, 'EnquiryManager/upcoming_surgeries.html', {
        'surgeries': surgeries,
        'doctors': doctors
    })

@login_required
def feedback(request):
    # Your logic here
    return render(request, 'EnquiryManager/feedback.html')

@login_required
def enquiry_list(request):
    search_query = request.GET.get('search', '')

    # Filter enquiries based on search input
    if search_query:
        enquiries = Enquiry.objects.filter(
            customer_name__icontains=search_query
        ).order_by('-enquiry_date')
    else:
        enquiries = Enquiry.objects.all().order_by('-enquiry_date')

    # Implement pagination (10 items per page)
    paginator = Paginator(enquiries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'enquiries': page_obj,
        'search_query': search_query
    }
    return render(request, 'EnquiryManager/enquiry_list.html', context)

@login_required
def enquiry_create(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enquiry_list')
    else:
        form = EnquiryForm()

    last_entries = Enquiry.objects.all().order_by('-enquiry_date')[:5]

    return render(request, 'EnquiryManager/enquiry_create.html', {
        'form': form,
        'last_entries': last_entries,
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
    states = State.objects.filter(name__icontains=term).order_by('name').values_list('name', flat=True).distinct()
    return JsonResponse(list(states), safe=False)

def city_autocomplete(request):
    term = request.GET.get('term', '')
    cities = City.objects.filter(name__icontains=term).order_by('name').values_list('name', flat=True).distinct()
    return JsonResponse(list(cities), safe=False)


def pincode_autocomplete(request):
    term = request.GET.get('term', '')
    pincodes = Enquiry.objects.filter(pincode__icontains=term).values_list('pincode', flat=True).distinct()
    return JsonResponse(list(pincodes), safe=False)

def enquiry_for_autocomplete(request):
    term = request.GET.get("term", "")
    results = Enquiry.objects.filter(enquiry_for__icontains=term) \
        .values_list("enquiry_for", flat=True).distinct().order_by("enquiry_for")
    return JsonResponse(list(results), safe=False)

@csrf_exempt
def save_state_city(request):
    if request.method == "POST":
        state_name = request.POST.get("state", "").strip().title()
        city_name = request.POST.get("city", "").strip().title()

        if state_name:
            state, _ = State.objects.get_or_create(name=state_name)
            if city_name:
                City.objects.get_or_create(name=city_name, state=state)

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)