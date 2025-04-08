from django.urls import path
from .views import (
    enquiry_list, enquiry_create, enquiry_edit, enquiry_delete,
    state_autocomplete, city_autocomplete, pincode_autocomplete, 
    consultation, surgery_schedule, feedback, enquiry_for_autocomplete,
    mark_as_processed, add_consultations, edit_consultation, add_surgery,
    today_surgeries, upcoming_surgeries
)

urlpatterns = [ 

    # Enquiries
    path('enquiries', enquiry_list, name='enquiry_list'),
    path('enquiries/new/', enquiry_create, name='enquiry_create'),
    path('enquiries/edit/<int:pk>/', enquiry_edit, name='enquiry_edit'),
    path('enquiries/delete/<int:enquiry_id>/', enquiry_delete, name='enquiry_delete'),

    # Search & Autocomplete
    path("search/states/", state_autocomplete, name="search_states"),
    path("search/cities/", city_autocomplete, name="search_cities"),
    path("search/pincodes/", pincode_autocomplete, name="search_pincodes"),
    path("autocomplete/enquiry-for/", enquiry_for_autocomplete, name="enquiry_for_autocomplete"),

    # Consultations
    path('consultation/', consultation, name='consultation'),
    path('consultation/mark/<int:id>/', mark_as_processed, name='mark_as_processed'),
    path('add_consultations/', add_consultations, name='add_consultations'),
    path('edit-consultation/<int:pk>/', edit_consultation, name='edit_consultation'),

    # Surgeries
    path('surgery_schedule/', surgery_schedule, name='surgery_schedule'),
    path('surgery/add/', add_surgery, name='add_surgery'),
    path('surgery/today/', today_surgeries, name='today_surgeries'),
    path('surgery/upcoming/', upcoming_surgeries, name='upcoming_surgeries'),

    #Feedback
    path('feedback/', feedback, name='feedback'),
]
