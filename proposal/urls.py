from django.urls import path
from proposal import views

app_name = 'proposal'

urlpatterns = [
    path('', views.ProposalIndexView.as_view(), name='proposal-index'),
    path('input', views.proposal_input, name='proposal-input'),
    path('detail/<int:pk>', views.ProposalDetailView.as_view(), name='detail-proposal'),
    path('edit/<int:pk>', views.proposal_edit, name='edit-proposal'),
    path('delete/<int:pk>', views.proposal_delete, name='delete-proposal'),
    path('approval/<int:pk>', views.proposal_approval, name='proposal-approval'),
    path('approval/kepsek/<int:pk>', views.proposal_approval_kepsek, name='proposal-approval-kepsek'),
    path('approval/bendahara/<int:pk>', views.proposal_approval_bendahara, name='proposal-approval-bendahara'),
    path('approval/transfer/<int:pk>', views.proposal_bukti_transfer, name='proposal-approval-transfer'),
    path('inventaris/input', views.proposal_inventaris_input, name='proposal-inventaris-input'),
    path('inventaris/detail/<int:pk>', views.proposal_inventaris_detail, name='detail-proposal-inventaris'),
    path('inventaris/edit/<int:pk>', views.proposal_inventaris_edit, name='edit-inventaris-proposal'),
    path('inventaris/delete/<int:pk>', views.proposal_inventaris_delete, name='delete-inventaris-proposal'),
    path('inventaris/approval/<int:pk>', views.proposal_inventaris_approval, name='proposal-inventaris-approval'),
    path('inventaris/approval/kepsek/<int:pk>', views.proposal_inventaris_approval_kepsek, name='proposal-inventaris-approval-kepsek'),
    path('inventaris/approval/bendahara/<int:pk>', views.proposal_inventaris_approval_bendahara, name='proposal-inventaris-approval-bendahara'),
    path('inventaris/approval/transfer/<int:pk>', views.proposal_inventaris_bukti_transfer, name='proposal-inventaris-approval-transfer'),
]
