from django.urls import path
from .views import upload_ticket, download_accounting_excel, download_cumulative_excel, view_history, filter_accounting_data, manage_budget, get_ticket_details, update_ticket, save_ticket_analysis

urlpatterns = [
    path('', upload_ticket, name='upload_ticket'),
    path('download-accounting-excel/', download_accounting_excel, name='download_accounting_excel'),
    path('download-cumulative-excel/', download_cumulative_excel, name='download_cumulative_excel'),
    path('history/', view_history, name='view_history'),
    path('filter-accounting-data/', filter_accounting_data, name='filter_accounting_data'),
    path('manage-budget/', manage_budget, name='manage_budget'),
    path('ticket/<int:ticket_id>/', get_ticket_details, name='get_ticket_details'),
    path('ticket/<int:ticket_id>/update/', update_ticket, name='update_ticket'),
    path('save-ticket-analysis/', save_ticket_analysis, name='save_ticket_analysis'),
]
