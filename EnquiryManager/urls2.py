from django.urls import path
from . import views
from .views import (
    enquiry_list, enquiry_create, enquiry_edit, enquiry_delete,
    state_autocomplete, city_autocomplete, pincode_autocomplete, 
    consultation, surgeries, schedule_surgery, enquiry_for_autocomplete,
    mark_as_processed, add_consultation, edit_consultation, add_consultation_from_enquiry, 
    reschedule, pending_enquiries, feedback,
generate_qr_code 
)

urlpatterns = [
    # Enquiries
    path('enquiry/create/', views.enquiry_create, name='enquiry_create'),
    path('enquiry/list/', views.enquiry_list, name='enquiry_list'),
    path('enquiry/edit/<int:enquiry_id>/', views.enquiry_edit, name='enquiry_edit'),
    path('enquiry/delete/<int:enquiry_id>/', views.enquiry_delete, name='enquiry_delete'),
    path('enquiry/pending/', views.pending_enquiries, name='pending_enquiries'),
    path('enquiry/state-autocomplete/', views.state_autocomplete, name='state_autocomplete'),
    path('enquiry/city-autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('enquiry/save-state-city/', views.save_state_city, name='save_state_city'),
    path('enquiry/pincode-autocomplete/', views.pincode_autocomplete, name='pincode_autocomplete'),
    path('enquiry/enquiry-for-autocomplete/', views.enquiry_for_autocomplete, name='enquiry_for_autocomplete'),
    
    # Consultations
    path('consultation/', views.consultation, name='consultation'),
    path('consultation/complete/<int:enquiry_id>/', views.complete_consultation, name='complete_consultation'),
    path('consultation/reschedule/<int:enquiry_id>/', views.reschedule, name='reschedule'),
    path('consultation/add/', views.add_consultation, name='add_consultation'),
    path('consultation/edit/<int:enquiry_id>/', views.edit_consultation, name='edit_consultation'),
    path('consultation/mark-processed/<int:id>/', views.mark_as_processed, name='mark_as_processed'),
    path('consultation/add-from-enquiry/<int:enquiry_id>/', views.add_consultation_from_enquiry, name='add_consultation_from_enquiry'),

    # Surgeries
    path('surgery/schedule/<int:enquiry_id>/', views.schedule_surgery, name='schedule_surgery'),
    
    # Add more URLs as per your needs
]
urlpatterns = [ 

    # Enquiries
    path('enquiries/', enquiry_list, name='enquiry_list'),
    path('enquiries/new/', enquiry_create, name='enquiry_create'),
    path('enquiries/edit/<int:pk>/', enquiry_edit, name='enquiry_edit'),
    path('enquiries/delete/<int:enquiry_id>/', enquiry_delete, name='enquiry_delete'),
    path('pending-enquiries/', pending_enquiries, name='pending_enquiries'),

    # Search & Autocomplete
    path("search/states/", state_autocomplete, name="search_states"),
    path("search/cities/", city_autocomplete, name="search_cities"),
    path("search/pincodes/", pincode_autocomplete, name="search_pincodes"),
    path("autocomplete/enquiry-for/", enquiry_for_autocomplete, name="enquiry_for_autocomplete"),

    # Consultations
    path('consultation/', consultation, name='consultation'),
    path('consultation/reschedule/<int:consultation_id>/', reschedule, name='reschedule_consultation'),
    path('enquiry/consultation/from/<int:enquiry_id>/', add_consultation_from_enquiry, name='add_consultation_from_enquiry'),
    path('consultation/mark/<int:id>/', mark_as_processed, name='mark_as_processed'),
    path('consultation/add/', add_consultation, name='add_consultation'),
    path('consultation/edit/<int:pk>/', edit_consultation, name='edit_consultation'),
    path('consultation/<int:consultation_id>/qr/', consultation_qr, name='consultation_qr'),  # ✅ QR for Consultation

    # Surgeries
    path('surgeries/', surgeries, name='surgeries'), 
    path('surgery/schedule/<int:consultation_id>/', schedule_surgery, name='schedule_surgery_module'),
    path('surgery/add/', reschedule_surgery, name='add_surgery'),

    # Feedback
    path('feedback/', feedback, name='feedback'),
]
