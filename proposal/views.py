from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from proposal.models import *
from proposal.forms import *


# Create your views here.

def index(request):
    proposal = Proposal.objects.all()
    jumlah = Proposal.objects.aggregate(Sum('anggaran_biaya'))
    jumlah_diterima = Proposal.objects.filter(Q(proposalstatus__is_wakasek="Accepted") & Q(proposalstatuskepsek__is_kepsek="Accepted")).aggregate(Sum('anggaran_biaya'))
    jumlah_ditolak = Proposal.objects.filter(Q(proposalstatus__is_wakasek="Rejected") | Q(proposalstatuskepsek__is_kepsek="Rejected")).aggregate(Sum('anggaran_biaya'))
    diterima = ProposalStatus.objects.filter(is_wakasek="Accepted")
    diterima_kepsek = ProposalStatusKepsek.objects.filter(is_kepsek="Accepted")
    diterima_bendahara = ProposalStatusBendahara.objects.filter(is_bendahara="Accepted")
    context = {
        'proposal': proposal,
        'jumlah': jumlah,
        'jumlah_diterima': jumlah_diterima,
        'jumlah_ditolak': jumlah_ditolak,
        'diterima': diterima,
        'diterima_kepsek': diterima_kepsek,
        'diterima_bendahara': diterima_bendahara,
    }
    return render(request, 'proposal.html', context)


def proposal_detail(request, pk):
    data = get_object_or_404(Proposal, id=pk)
    status = ProposalStatus.objects.all()
    context = {
        'data': data,
        'status': status,
    }
    return render(request, 'proposal-detail.html', context)
@login_required(login_url='/login/')
def proposal_input(request):
    if request.method == "POST":
        nama_event = request.POST.get('nama_event')
        obj = Proposal.objects.filter(nama_event__icontains=nama_event)
        if obj:
            forms = ProposalForm()
            messages.error(request, "Proposal untuk event ini sudah ada. Silahkan cari di menu atau buat yang baru.")
        else:
            forms = ProposalForm(request.POST, request.FILES)
            if forms.is_valid():
                forms.save()
                p = get_object_or_404(Proposal, nama_event=nama_event)
                status1 = ProposalStatus.objects.create(
                    proposal=p,
                    is_wakasek="Pending",
                    alasan_wakasek="",
                )
                p_status1 = get_object_or_404(ProposalStatus, proposal=p.id)
                status2 = ProposalStatusKepsek.objects.create(
                    proposal=p,
                    status_wakasek=p_status1,
                    is_kepsek="Pending",
                    alasan_kepsek=""
                )
                p_status2 = get_object_or_404(ProposalStatusKepsek, proposal=p.id)
                status3 = ProposalStatusBendahara.objects.create(
                    proposal=p,
                    status_kepsek=p_status2,
                    is_bendahara="Pending",
                    alasan_bendahara=""
                )
                status1.save()
                status2.save()
                status3.save()

                return redirect('proposal:proposal-index')
            else:
                forms = ProposalForm(request.POST, request.FILES)
                messages.error(request, "Yang kamu isi ada yang salah. Silahkan cek lagi.")
    else:
        forms = ProposalForm()
    context = {
        'forms': forms,
    }
    return render(request, 'proposal-input.html', context)

@login_required(login_url='/login/')
def proposal_edit(request, pk):
    data = get_object_or_404(Proposal, id=pk)

    if request.method == "POST":
        forms = ProposalEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('proposal:proposal-index')
        # else:
        #     forms = ProposalForm(instance=data)
        #     messages.error(request, "Data yang kamu isi ada yang salah. Silahkan periksa lagi.")
    else:
        forms = ProposalEditForm(instance=data)

    context = {
        'forms': forms,
    }

    return render(request, 'proposal-edit.html', context)

@login_required(login_url='/login/')
def proposal_delete(request, pk):
    data = get_object_or_404(Proposal, id=pk)

    if request.method == "POST":
        data.delete()
        return redirect('proposal:proposal-index')

    context = {
        'data': data,
    }
    return render(request, 'proposal-delete.html', context)


@login_required(login_url='/login/')
def proposal_approval(request, pk):
    status = Proposal.objects.get(id=pk)
    data = get_object_or_404(ProposalStatus, proposal=status.id)
    if request.method == "POST":
        forms = StatusProposalForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('proposal:proposal-index')
    else:
        forms = StatusProposalForm(instance=data)
    context = {
        'forms': forms,
    }
    return render(request, 'proposal-approval.html', context)
@login_required(login_url='/login/')
def proposal_approval_kepsek(request, pk):
    status = Proposal.objects.get(id=pk)
    data = ProposalStatusKepsek.objects.get(proposal=status.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalKepsekForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Wakasek Ekstrakurikuler.")

    else:
        forms = StatusProposalKepsekForm(instance=data)

    context = {
        'forms': forms,
        'status': status,
        'data': data,
    }
    return render(request, 'proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_approval_bendahara(request, pk):
    status = Proposal.objects.get(id=pk)
    data = ProposalStatusBendahara.objects.get(proposal=status.id)

    if request.method == "POST":
        if data.status_kepsek.is_kepsek == "Accepted":
            forms = StatusProposalBendaharaForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalBendaharaForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Kepala Sekolah.")
    else:
        forms = StatusProposalBendaharaForm(instance=data)

    context = {
        'forms': forms,
        'status': status,
    }
    return render(request, 'proposal-approval.html', context)