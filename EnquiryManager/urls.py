from django.urls import path
from . import views


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
    path('surgeries/', views.surgeries, name='surgeries'), 
    path('surgery/schedule/<int:enquiry_id>/', views.schedule_surgery, name='schedule_surgery'),
    
        # Feedback
    path('feedback/', views.feedback, name='feedback'),
]
