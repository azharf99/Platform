import requests
from django.conf import settings
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView

from proposal.forms import ProposalForm, ProposalEditForm, StatusProposalForm, StatusProposalKepsekForm, StatusProposalBendaharaForm, ProposalInventarisForm, ProposalInventarisEditForm, StatusProposalInventarisForm, StatusProposalInventarisKepsekForm, StatusProposalInventarisBendaharaForm
from proposal.models import Proposal, ProposalStatus, ProposalStatusBendahara, ProposalStatusKepsek, ProposalInventaris, ProposalInventarisStatus, ProposalInventarisStatusKepsek, ProposalInventarisStatusBendahara
from userlog.models import UserLog
token = settings.TOKEN

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
                phone = request.user.teacher.no_hp
                message = f'''*[NOTIFIKASI]*
Anda berhasil mengajukan proposal acara *{p.nama_event}* dengan anggaran dana *{p.anggaran_biaya}* dan penanggung jawab *{p.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                requests.get(url)

                phone = '081293034867' #no ust panji
                message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {"Ustadz Panji Asmara, S.Pd."}, ada proposal acara baru yang masuk dengan rincian:

*Nama proposal : {p.nama_event}*
*Anggaran dana : {p.anggaran_biaya}*
*Penanggung jawab : {p.penanggungjawab}*

Mohon sekiranya ustadz dapat meninjau proposal acara tersebut pada aplikasi.

Link App:
https://pmbp.smasitalbinaa.com/proposal

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/approval/{p.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                requests.get(url)

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

            phone = request.user.teacher.no_hp
            message = f'''*[NOTIFIKASI]*
Anda berhasil mengubah data proposal acara *{data.nama_event}* dengan anggaran dana *{data.anggaran_biaya}* dan penanggung jawab *{data.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            requests.get(url)
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

        phone = request.user.teacher.no_hp
        message = f'''*[NOTIFIKASI]*
Anda berhasil menghapus data proposal acara *{data.nama_event}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
        url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

        response = requests.get(url)
        print(response.text)

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
    status = Proposal.objects.get(id=pk)
    data = get_object_or_404(ProposalStatus, proposal=status.id)
    if request.method == "POST":
        forms = StatusProposalForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="APPROVAL",
                app="PROPOSAL_WAKASEK",
                message="Wakasek berhasil melakukan approval pada proposal acara {} dengan status {}".format(status, data.is_wakasek)
            )

            phone = request.user.teacher.no_hp
            message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal acara *{status.nama_event}* dengan status *{data.is_wakasek}* dan komentar *{data.alasan_wakasek}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            phone = '081398176123' #no kepsek
            message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {"Agung Wahyu Adhy, Lc."}, Ada proposal acara baru yang masuk dengan rincian:

*Nama proposal : {status.nama_event}*
*Anggaran dana : {status.anggaran_biaya}*
*Penanggung jawab : {status.penanggungjawab}*
*Keputusan Wakasek saat ini: {data.is_wakasek}*
*Komentar dari Wakasek: {data.alasan_wakasek}*

Mohon sekiranya ustadz dapat meninjau proposal acara tersebut pada aplikasi.

Link Apps:
https://pmbp.smasitalbinaa.com/
Silahkan login terlebih dahulu, lalu pilih *Menu* dan pilih *Proposal*.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/approval/kepsek/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            phone = status.penanggungjawab.no_hp
            message = f'''*[NOTIFIKASI]*
Proposal acara anda dengan judul *{status.nama_event}* telah *ditinjau oleh Wakasek Ekstrakurikuler*.
Status Proposal : {data.is_wakasek}
Komentar Wakasek: {data.alasan_wakasek}
Mohon sekiranya Anda dapat meninjau status proposal acara tersebut pada aplikasi.
https://pmbp.smasitalbinaa.com/proposal

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            return redirect('proposal:proposal-index')
    else:
        forms = StatusProposalForm(instance=data)
    context = {
        'forms': forms,
        'status': {
            'id' : status.id,
            'nama_event': status.nama_event
        }
    }
    return render(request, 'new_proposal-approval.html', context)


@login_required(login_url='/login/')
def proposal_approval_kepsek(request, pk):
    if not request.user.username == "agung_wa":
        return redirect('restricted')
    status = get_object_or_404(Proposal, id=pk)
    data = get_object_or_404(ProposalStatusKepsek, proposal_id=status.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_KEPSEK",
                    message="Kepala Sekolah berhasil melakukan approval pada proposal acara {} dengan status {}".format(status, data.is_kepsek)
                )

                phone = request.user.teacher.no_hp
                message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal acara *{status.nama_event}* dengan status *{data.is_kepsek}* dan komentar *{data.alasan_kepsek}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = '085295188663' #no bendahara
                message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {"Ustadz Chevi Indrayadi, S.Si"}, Ada proposal acara baru yang masuk dengan rincian:

*Nama proposal : {status.nama_event}*
*Anggaran dana : {status.anggaran_biaya}*
*Penanggung jawab : {status.penanggungjawab}*

*Keputusan Wakasek saat ini: {data.status_wakasek.is_wakasek}*
*Komentar dari Wakasek: {data.status_wakasek.alasan_wakasek}*

*Keputusan Kepala Sekolah saat ini: {data.is_kepsek}*
*Komentar dari Kepala Sekolah: {data.alasan_kepsek}*

Mohon sekiranya ustadz dapat meninjau proposal acara tersebut pada aplikasi.

Link Apps:
https://pmbp.smasitalbinaa.com/
Silahkan login terlebih dahulu, lalu pilih *Menu* dan pilih *Proposal*.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/approval/bendahara/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = status.penanggungjawab.no_hp
                message = f'''*[NOTIFIKASI]*
Proposal acara anda dengan judul *{status.nama_event}* telah *ditinjau oleh Wakasek dan Kepala Sekolah*.
Status Proposal : {data.is_kepsek}
Komentar Kepsek : {data.alasan_kepsek}
Mohon sekiranya Anda dapat meninjau status proposal acara tersebut pada aplikasi.
https://pmbp.smasitalbinaa.com/proposal

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

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
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_approval_bendahara(request, pk):
    if not request.user.username == "chevi_indrayadi":
        return redirect('restricted')
    status = Proposal.objects.get(id=pk)
    data = ProposalStatusBendahara.objects.get(proposal=status.id)

    if request.method == "POST":
        if data.status_kepsek.is_kepsek == "Accepted":
            forms = StatusProposalBendaharaForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_BENDAHARA",
                    message="Bendahara berhasil melakukan approval pada proposal acara {} dengan status {}".format(status, data.is_bendahara)
                )

                phone = request.user.teacher.no_hp
                message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal acara *{status.nama_event}* dengan status *{data.is_bendahara}* dan komentar *{data.alasan_bendahara}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = '081293034867' #no ust panji
                message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {'Ustadz Panji Asmara, S.Pd.'}, Proposal acara *{status.nama_event}*

*Telah di-approve oleh Bendahara dan dana dikirim melalui nomer rekening Ustadz Panji atau PJ yang bersangkutan.*

Mohon sekiranya ustadz dapat meninjau proposal acara tersebut pada aplikasi.

Link App:
https://pmbp.smasitalbinaa.com/proposal

Bukti transfer dana:
https://pmbp.smasitalbinaa.com/proposal/approval/transfer/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = status.penanggungjawab.no_hp
                message = f'''*[NOTIFIKASI]*
Proposal acara anda dengan judul *{status.nama_event}* telah *ditinjau oleh Wakasek, Kepala Sekolah dan Bendahara*.
Status Proposal     : {data.is_bendahara}
Komentar Bendahara  : {data.alasan_bendahara}
Mohon sekiranya Anda dapat meninjau status proposal acara tersebut pada aplikasi.

https://pmbp.smasitalbinaa.com/proposal

Bukti transfer dana (jika sudah ada):
https://pmbp.smasitalbinaa.com/proposal/approval/transfer/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)
                
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

                phone = request.user.teacher.no_hp
                message = f'''*[NOTIFIKASI]*
Anda berhasil mengajukan proposal pengadaan barang *{p.judul_proposal}* dengan anggaran dana *{p.anggaran_biaya}* dan penanggung jawab *{p.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = '081293034867' #no ust panji
                message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {"Ustadz Panji Asmara, S.Pd."}, ada proposal acara baru yang masuk dengan rincian:

*Nama proposal : {p.judul_proposal}*
*Anggaran dana : {p.anggaran_biaya}*
*Penanggung jawab : {p.penanggungjawab}*

Mohon sekiranya ustadz dapat meninjau proposal pengadaan barang tersebut pada aplikasi.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/approval/{p.id}

Syukron.
_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

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
            phone = request.user.teacher.no_hp
            message = f'''*[NOTIFIKASI]*
Anda berhasil mengubah proposal pengadaan barang *{data.judul_proposal}* dengan anggaran dana *{data.anggaran_biaya}* dan penanggung jawab *{data.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

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
        phone = request.user.teacher.no_hp
        message = f'''*[NOTIFIKASI]*
Anda berhasil menghapus proposal pengadaan barang *{data.judul_proposal}* dengan anggaran dana *{data.anggaran_biaya}* dan penanggung jawab *{data.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
        url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

        response = requests.get(url)
        print(response.text)

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
    status = ProposalInventaris.objects.get(id=pk)
    data = get_object_or_404(ProposalInventarisStatus, proposal=status.id)
    if request.method == "POST":
        forms = StatusProposalInventarisForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="APPROVAL",
                app="PROPOSAL_WAKASEK",
                message="Wakasek berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(status, data.is_wakasek)
            )

            phone = request.user.teacher.no_hp
            message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal inventaris/pengadaan *{status.judul_proposal}* dengan status *{data.is_wakasek}* dan komentar *{data.is_wakasek}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            phone = '081398176123' #no Kepsek
            message = f'''*[NOTIFIKASI]*
Ada proposal inventaris/pengadaan baru yang masuk dengan rincian:

*Nama proposal : {status.judul_proposal}*
*Anggaran dana : {status.anggaran_biaya}*
*Penanggung jawab : {status.penanggungjawab}*
*Keputusan Wakasek saat ini: {data.is_wakasek}*
*Komentar dari Wakasek: {data.status_wakasek}*

Mohon sekiranya ustadz dapat meninjau proposal inventaris/pengadaan tersebut pada aplikasi.

Link Apps:
https://pmbp.smasitalbinaa.com/
Silahkan login terlebih dahulu, lalu pilih *Menu* dan pilih *Proposal*.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/inventaris/approval/kepsek/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            phone = status.penanggungjawab.no_hp
            message = f'''*[NOTIFIKASI]*
Proposal inventaris/pengadaan anda dengan judul *{status.judul_proposal}* telah *ditinjau oleh Wakasek Ekstrakurikuler*.
Status Proposal : {data.is_wakasek}
Komentar Wakasek: {data.alasan_wakasek}
Mohon sekiranya Anda dapat meninjau status proposal inventaris/pengadaan tersebut pada aplikasi.
https://pmbp.smasitalbinaa.com/proposal

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
            url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

            response = requests.get(url)
            print(response.text)

            return redirect('proposal:proposal-index')
    else:
        forms = StatusProposalInventarisForm(instance=data)
    context = {
        'forms': forms,
        'status': {
            'id' : status.id,
            'nama_event': status.judul_proposal
        },
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_approval_kepsek(request, pk):
    if not request.user.username == "agung_wa":
        return redirect('restricted')
    status = ProposalInventaris.objects.get(id=pk)
    data = ProposalInventarisStatus.objects.get(proposal=status.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalInventarisKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_KEPSEK",
                    message="Kepala Sekolah berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(status, data.is_kepsek)
                )

                phone = request.user.teacher.no_hp
                message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal inventaris/pengadaan *{status.judul_proposal}* dengan status *{data.is_kepsek}* dan komentar *{data.is_kepsek}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = '085295188663' #no Bendahara
                message = f'''*[NOTIFIKASI]*
Ada proposal inventaris/pengadaan baru yang masuk dengan rincian:

*Nama proposal : {status.judul_proposal}*
*Anggaran dana : {status.anggaran_biaya}*
*Penanggung jawab : {status.penanggungjawab}*

*Keputusan Wakasek saat ini: {data.is_wakasek}*
*Komentar dari Wakasek: {data.status_wakasek}*

*Keputusan Kepala Sekolah saat ini: {data.is_kepsek}*
*Komentar dari Kepala Sekolah: {data.is_kepsek}*

Mohon sekiranya ustadz dapat meninjau proposal inventaris/pengadaan tersebut pada aplikasi.

Link Apps:
https://pmbp.smasitalbinaa.com/
Silahkan login terlebih dahulu, lalu pilih *Menu* dan pilih *Proposal*.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal/inventaris/approval/kepsek/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = status.penanggungjawab.no_hp
                message = f'''*[NOTIFIKASI]*
Proposal inventaris/pengadaan anda dengan judul *{status.judul_proposal}* telah *ditinjau oleh Kepala Sekolah*.
Status Proposal : {data.is_kepsek}
Komentar Kepsek: {data.is_wakasek}
Mohon sekiranya Anda dapat meninjau status proposal inventaris/pengadaan tersebut pada aplikasi.
https://pmbp.smasitalbinaa.com/proposal

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalInventarisKepsekForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Wakasek Ekstrakurikuler.")

    else:
        forms = StatusProposalInventarisKepsekForm(instance=data)

    context = {
        'forms': forms,
        'status': status,
        'data': data,
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)

@login_required(login_url='/login/')
def proposal_inventaris_approval_bendahara(request, pk):
    if not request.user.username == "chevi_indrayadi":
        return redirect('restricted')
    status = ProposalInventaris.objects.get(id=pk)
    data = ProposalInventarisStatusBendahara.objects.get(proposal=status.id)

    if request.method == "POST":
        if data.status_kepsek.is_kepsek == "Accepted":
            forms = StatusProposalInventarisBendaharaForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_BENDAHARA",
                    message="Bendahara berhasil melakukan approval pada proposal inventaris/pengadaan {} dengan status {}".format(status, data.is_bendahara)
                )

                phone = request.user.teacher.no_hp #no Bendahara
                message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal inventaris/pengadaan *{status.judul_proposal}* dengan status *{data.is_bendahara}* dan komentar *{data.is_bendahara}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = '081293034867' #no ust panji
                message = f'''*[NOTIFIKASI]*
Proposal *{status.judul_proposal}* *Telah di-approve oleh Bendahara dan dana dikirim melalui nomer rekening Ustadz Panji atau PJ yang bersangkutan.*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.

Bukti transfer dana:
https://pmbp.smasitalbinaa.com/proposal/approval/transfer/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                phone = status.penanggungjawab.no_hp #no PJ proposal
                message = f'''*[NOTIFIKASI]*
Proposal inventaris/pengadaan anda dengan judul *{status.judul_proposal}* telah *ditinjau oleh Wakasek, Kepala Sekolah dan Bendahara*.
Status Proposal     : {data.is_bendahara}
Komentar Bendahara  : {data.alasan_bendahara}
Mohon sekiranya Anda dapat meninjau status proposal inventaris/pengadaan tersebut pada aplikasi.

https://pmbp.smasitalbinaa.com/proposal

Bukti transfer dana (jika sudah ada):
https://pmbp.smasitalbinaa.com/proposal/approval/transfer/{status.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                print(response.text)

                return redirect('proposal:proposal-index')
        else:
            forms = StatusProposalInventarisBendaharaForm(instance=data)
            messages.error(request, "Mohon maaf, proposal belum/tidak di-approve oleh Kepala Sekolah.")
    else:
        forms = StatusProposalInventarisBendaharaForm(instance=data)

    context = {
        'forms': forms,
        'status': status,
        'tipe': 'inventaris',
    }
    return render(request, 'new_proposal-approval.html', context)