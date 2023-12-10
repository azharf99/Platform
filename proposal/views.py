import requests

from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView

from proposal.forms import ProposalForm, ProposalEditForm, StatusProposalForm, StatusProposalKepsekForm, StatusProposalBendaharaForm, ProposalInventarisForm, ProposalInventarisEditForm, StatusProposalInventarisForm, StatusProposalInventarisKepsekForm, StatusProposalInventarisBendaharaForm
from proposal.models import Proposal, ProposalStatus, ProposalStatusBendahara, ProposalStatusKepsek, ProposalInventaris, ProposalInventarisStatus, ProposalInventarisStatusKepsek, ProposalInventarisStatusBendahara
from userlog.models import UserLog
from dashboard.whatsapp import send_whatsapp_proposal, send_whatsapp_proposal_wakasek, send_whatsapp_proposal_approval, send_whatsapp_proposal_kepsek, send_whatsapp_proposal_review, send_whatsapp_proposal_bendahara, send_whatsapp_proposal_finish


# Create your views here.
class ProposalIndexView(ListView):
    model = Proposal
    template_name = 'new_proposal.html'
    paginate_by = 5
    queryset = Proposal.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["proposal_inventaris"] = ProposalInventaris.objects.all().order_by('-created_at')
        context["jumlah"] = Proposal.objects.aggregate(Sum('anggaran_biaya'))
        context["jumlah_diterima"] = Proposal.objects.filter(proposalstatusbendahara__is_bendahara="Accepted")
        context["jumlah_pending"] = Proposal.objects.filter(proposalstatusbendahara__is_bendahara="Pending")
        context["dana_diterima"] = Proposal.objects.filter(proposalstatusbendahara__is_bendahara="Accepted").aggregate(Sum('anggaran_biaya'))
        context["dana_pending"] = Proposal.objects.filter(proposalstatusbendahara__is_bendahara="Pending").aggregate(Sum('anggaran_biaya'))
        context["dana_ditolak"] = Proposal.objects.filter(proposalstatus__is_wakasek="Rejected").aggregate(Sum('anggaran_biaya'))
        return context

class ProposalDetailView(DetailView):
    model = Proposal
    template_name = 'new_proposal-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipe'] = 'lomba'
        context['status'] = ProposalStatus.objects.all()
        return context

def proposal_inventaris_detail(request, pk):
    data = get_object_or_404(ProposalInventaris, id=pk)
    status = ProposalStatus.objects.all()
    context = {
        'data': data,
        'status': status,
        'tipe': 'barang'
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
                ProposalStatus.objects.create(
                    proposal=p,
                    is_wakasek="Pending",
                    alasan_wakasek="",
                )
                p_status1 = get_object_or_404(ProposalStatus, proposal=p.id)
                ProposalStatusKepsek.objects.create(
                    proposal=p,
                    status_wakasek=p_status1,
                    is_kepsek="Pending",
                    alasan_kepsek=""
                )
                p_status2 = get_object_or_404(ProposalStatusKepsek, proposal=p.id)
                ProposalStatusBendahara.objects.create(
                    proposal=p,
                    status_kepsek=p_status2,
                    is_bendahara="Pending",
                    alasan_bendahara=""
                )
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="PROPOSAL",
                    message="Berhasil mengajukan proposal acara {} dengan anggaran sebesar {} dan penanggung jawab {}".format(p.nama_event, p.anggaran_biaya, p.penanggungjawab)
                )
                send_whatsapp_proposal(request.user.teacher.no_hp, p, 'mengajukan', p.nama_event)
                send_whatsapp_proposal_wakasek('081293034867', p, '', "Ustadz Panji Asmara, S.Pd.", p.nama_event)

                return redirect('proposal:proposal-index')
            else:
                forms = ProposalForm(request.POST, request.FILES)
                messages.error(request, "Yang kamu isi ada yang salah. Silahkan cek lagi.")
    else:
        forms = ProposalForm()
    context = {
        'forms': forms,
        'name' : 'Lomba',
    }
    return render(request, 'new_proposal-input.html', context)

@login_required(login_url='/login/')
def proposal_edit(request, pk):
    data = get_object_or_404(Proposal, id=pk)
    if not data.penanggungjawab.user.username == request.user.username and not request.user.is_superuser:
        return redirect('restricted')

    if request.method == "POST":
        forms = ProposalEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="PROPOSAL",
                message="Berhasil mengubah data proposal acara {}".format(data)
            )

            send_whatsapp_proposal(request.user.teacher.no_hp, data, 'mengedit', data.nama_event)
            return redirect('proposal:proposal-index')
        else:
            forms = ProposalForm(instance=data)
            messages.error(request, "Data yang kamu isi ada yang salah. Silahkan periksa lagi.")
    else:
        forms = ProposalEditForm(instance=data)

    context = {
        'forms': forms,
    }

    return render(request, 'new_proposal-input.html', context)

@login_required(login_url='/login/')
def proposal_delete(request, pk):
    data = get_object_or_404(Proposal, id=pk)
    if not data.penanggungjawab.user.username == request.user.username and not request.user.is_superuser:
        return redirect('restricted')

    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="CHANGE",
            app="PROPOSAL",
            message="Berhasil menghapus data proposal acara {}".format(data)
        )

        send_whatsapp_proposal(request.user.teacher.no_hp, data, 'menghapus', data.nama_event)

        data.delete()
        return redirect('proposal:proposal-index')

    context = {
        'data': data,
    }
    return render(request, 'new_proposal-delete.html', context)


@login_required(login_url='/login/')
def proposal_approval(request, pk):
    if not request.user.username == "panji_asmara":
        return redirect('restricted')
    proposal = Proposal.objects.get(id=pk)
    data = get_object_or_404(ProposalStatus, proposal=proposal.id)
    if request.method == "POST":
        forms = StatusProposalForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="APPROVAL",
                app="PROPOSAL_WAKASEK",
                message="Wakasek berhasil melakukan approval pada proposal acara {} dengan status {}".format(proposal, data.is_wakasek)
            )

            send_whatsapp_proposal_approval(request.user.teacher.no_hp, data, proposal.nama_event, data.is_wakasek, data.alasan_wakasek)
            send_whatsapp_proposal_kepsek('081398176123', proposal, data, '', "Ustadz Agung Wahyu Adhy, Lc., M.Pd.", proposal.nama_event)
            send_whatsapp_proposal_review(request.user.teacher.no_hp, proposal.nama_event, data)

            return redirect('proposal:proposal-index')
    else:
        forms = StatusProposalForm(instance=data)
    context = {
        'forms': forms,
        'status': {
            'id' : proposal.id,
            'nama_event': proposal.nama_event
        }
    }
    return render(request, 'new_proposal-approval.html', context)


@login_required(login_url='/login/')
def proposal_approval_kepsek(request, pk):
    if not request.user.username == "agung_wa":
        return redirect('restricted')
    proposal = get_object_or_404(Proposal, id=pk)
    data = get_object_or_404(ProposalStatusKepsek, proposal_id=proposal.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_KEPSEK",
                    message="Kepala Sekolah berhasil melakukan approval pada proposal acara {} dengan status {}".format(proposal, data.is_kepsek)
                )

                send_whatsapp_proposal_approval(request.user.teacher.no_hp, data, proposal.nama_event, data.is_kepsek, data.alasan_kepsek)
                send_whatsapp_proposal_bendahara('085295188663', proposal, data, '', "Ustadz Chevi Indrayadi, S.Si", proposal.nama_event)
                send_whatsapp_proposal_review(request.user.teacher.no_hp, proposal.nama_event, data)

                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalKepsekForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Wakasek Ekstrakurikuler.")

    else:
        forms = StatusProposalKepsekForm(instance=data)

    context = {
        'forms': forms,
        'status': proposal,
        'data': data,
    }
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_approval_bendahara(request, pk):
    if not request.user.username == "chevi_indrayadi":
        return redirect('restricted')
    proposal = Proposal.objects.get(id=pk)
    data = ProposalStatusBendahara.objects.get(proposal=proposal.id)

    if request.method == "POST":
        if data.status_kepsek.is_kepsek == "Accepted":
            forms = StatusProposalBendaharaForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_BENDAHARA",
                    message="Bendahara berhasil melakukan approval pada proposal acara {} dengan status {}".format(proposal, data.is_bendahara)
                )

                send_whatsapp_proposal_approval(request.user.teacher.no_hp, data, proposal.nama_event, data.is_kepsek, data.alasan_kepsek)
                send_whatsapp_proposal_finish(proposal.penanggungjawab.no_hp, proposal, '', proposal.penanggungjawab, proposal.nama_event)
                send_whatsapp_proposal_finish('081293034867', proposal, '', 'Ustadz Panji Asmara, S.Pd.', proposal.nama_event)
                
                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalBendaharaForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Kepala Sekolah.")
    else:
        forms = StatusProposalBendaharaForm(instance=data)

    context = {
        'forms': forms,
        'status': proposal,
    }
    return render(request, 'new_proposal-approval.html', context)


def proposal_bukti_transfer(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    context = {
        'proposal': proposal,
    }
    return render(request, 'proposal-approval-transfer.html', context)


def proposal_inventaris_bukti_transfer(request, pk):
    proposal = get_object_or_404(ProposalInventaris, id=pk)
    context = {
        'proposal': proposal,
    }
    return render(request, 'proposal-approval-transfer.html', context)


@login_required(login_url='/login/')
def proposal_inventaris_input(request):
    if request.method == "POST":
        judul = request.POST.get('judul_proposal')
        obj = ProposalInventaris.objects.filter(judul_proposal__icontains=judul)
        if obj:
            forms = ProposalInventarisForm()
            messages.error(request, "Proposal untuk inventaris ini sudah ada. Silahkan cari di menu atau buat yang baru.")
        else:
            forms = ProposalInventarisForm(request.POST, request.FILES)
            if forms.is_valid():
                forms.save()
                p = get_object_or_404(ProposalInventaris, judul_proposal=judul)
                ProposalInventarisStatus.objects.create(
                    proposal=p,
                    is_wakasek="Pending",
                    alasan_wakasek="",
                )
                p_status1 = get_object_or_404(ProposalInventarisStatus, proposal=p.id)
                ProposalInventarisStatusKepsek.objects.create(
                    proposal=p,
                    status_wakasek=p_status1,
                    is_kepsek="Pending",
                    alasan_kepsek=""
                )
                p_status2 = get_object_or_404(ProposalInventarisStatusKepsek, proposal=p.id)
                ProposalInventarisStatusBendahara.objects.create(
                    proposal=p,
                    status_kepsek=p_status2,
                    is_bendahara="Pending",
                    alasan_bendahara=""
                )

                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="PROPOSAL",
                    message="Berhasil mengajukan proposal inventaris/pengadaan {} dengan anggaran sebesar {} dan penanggung jawab {}".format(p.judul_proposal, p.anggaran_biaya, p.penanggungjawab)
                )

                send_whatsapp_proposal(request.user.teacher.no_hp, p, 'mengajukan', p.judul_proposal)
                send_whatsapp_proposal_wakasek('081293034867', p, '/inventaris', "Ustadz Panji Asmara, S.Pd.", p.judul_proposal)

                return redirect('proposal:proposal-index')
            else:
                forms = ProposalInventarisForm(request.POST, request.FILES)
                messages.error(request, "Yang kamu isi ada yang salah. Silahkan cek lagi.")
    else:
        forms = ProposalInventarisForm()
    context = {
        'forms': forms,
        'name' : 'Inventaris',
    }
    return render(request, 'proposal-input.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_edit(request, pk):
    data = get_object_or_404(ProposalInventaris, id=pk)
    if not data.penanggungjawab.user.username == request.user.username and not request.user.is_superuser:
        return redirect('restricted')

    if request.method == "POST":
        forms = ProposalInventarisEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="PROPOSAL",
                message="Berhasil mengubah data proposal inventaris/pengadaan {}".format(data)
            )

            send_whatsapp_proposal(request.user.teacher.no_hp, data, 'mengubah', data.judul_proposal)

            return redirect('proposal:proposal-index')
        else:
            forms = ProposalInventarisEditForm(instance=data)
            messages.error(request, "Data yang kamu isi ada yang salah. Silahkan periksa lagi.")
    else:
        forms = ProposalInventarisEditForm(instance=data)

    context = {
        'forms': forms,
    }

    return render(request, 'proposal-edit.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_delete(request, pk):
    data = get_object_or_404(ProposalInventaris, id=pk)
    if not data.penanggungjawab.user.username == request.user.username and not request.user.is_superuser:
        return redirect('restricted')

    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="CHANGE",
            app="PROPOSAL",
            message="Berhasil menghapus data proposal inventaris/pengadaan {}".format(data)
        )

        send_whatsapp_proposal(request.user.teacher.no_hp, data, 'menghapus', data.judul_proposal)

        data.delete()
        return redirect('proposal:proposal-index')

    context = {
        'data': data,
    }
    return render(request, 'proposal-delete.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_approval(request, pk):
    if not request.user.username == "panji_asmara":
        return redirect('restricted')
    proposal = ProposalInventaris.objects.get(id=pk)
    data = get_object_or_404(ProposalInventarisStatus, proposal=proposal.id)
    if request.method == "POST":
        forms = StatusProposalInventarisForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="APPROVAL",
                app="PROPOSAL_WAKASEK",
                message="Wakasek berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(proposal, data.is_wakasek)
            )

            send_whatsapp_proposal_approval(request.user.teacher.no_hp, proposal.judul_proposal, data.is_wakasek, data.alasan_wakasek)
            send_whatsapp_proposal_kepsek('081398176123', proposal, data, '/inventaris', 'Ustadz Agung Wahyu Adhy, Lc., M.Pd.', proposal.judul_proposal)
            send_whatsapp_proposal_review(proposal.penanggungjawab.no_hp, proposal.judul_proposal, data)

            return redirect('proposal:proposal-index')
    else:
        forms = StatusProposalInventarisForm(instance=data)
    context = {
        'forms': forms,
        'status': {
            'id' : proposal.id,
            'nama_event': proposal.judul_proposal
        },
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_approval_kepsek(request, pk):
    if not request.user.username == "agung_wa":
        return redirect('restricted')
    proposal = ProposalInventaris.objects.get(id=pk)
    data = ProposalInventarisStatusKepsek.objects.get(proposal=proposal.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalInventarisKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_KEPSEK",
                    message="Kepala Sekolah berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(proposal, data.is_kepsek)
                )

                send_whatsapp_proposal_approval(request.user.teacher.no_hp, proposal.judul_proposal, data.is_kepsek, data.alasan_kepsek)
                send_whatsapp_proposal_bendahara('085295188663', proposal, data, '/inventaris', 'Ustadz Chevi Indrayadi, S.Si', proposal.judul_proposal)
                send_whatsapp_proposal_review(proposal.penanggungjawab.no_hp, proposal.judul_proposal, data)

                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalInventarisKepsekForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Wakasek Ekstrakurikuler.")

    else:
        forms = StatusProposalInventarisKepsekForm(instance=data)

    context = {
        'forms': forms,
        'status': proposal,
        'data': data,
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_approval_bendahara(request, pk):
    if not request.user.username == "chevi_indrayadi":
        return redirect('restricted')
    proposal = ProposalInventaris.objects.get(id=pk)
    data = ProposalInventarisStatusBendahara.objects.get(proposal=proposal.id)

    if request.method == "POST":
        if data.status_kepsek.is_kepsek == "Accepted":
            forms = StatusProposalInventarisBendaharaForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_BENDAHARA",
                    message="Bendahara berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(proposal, data.is_bendahara)
                )

                send_whatsapp_proposal_approval(request.user.teacher.no_hp, proposal.judul_proposal, data.is_bendahara, data.alasan_bendahara)
                send_whatsapp_proposal_finish('081293034867', proposal, '/approval', 'Panji Asmara, S.Pd', proposal.judul_proposal)
                send_whatsapp_proposal_finish(proposal.penanggungjawab.no_hp, proposal, '', proposal.penanggungjawab, proposal.judul_proposal)

                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalInventarisBendaharaForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Kepala Sekolah.")
    else:
        forms = StatusProposalInventarisBendaharaForm(instance=data)

    context = {
        'forms': forms,
        'status': proposal,
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)