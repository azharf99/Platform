from django.urls import path
from proposal import views

app_name = 'proposal'

urlpatterns = [
    path('', views.index, name='proposal-index'),
    path('input', views.proposal_input, name='proposal-input'),
    path('detail/<int:pk>', views.proposal_detail, name='detail-proposal'),
    path('edit/<int:pk>', views.proposal_edit, name='edit-proposal'),
    path('delete/<int:pk>', views.proposal_delete, name='delete-proposal'),
    path('approval/<int:pk>', views.proposal_approval, name='proposal-approval'),
    path('approval/kepsek/<int:pk>', views.proposal_approval_kepsek, name='proposal-approval-kepsek'),
    path('approval/bendahara/<int:pk>', views.proposal_approval_bendahara, name='proposal-approval-bendahara'),
]
