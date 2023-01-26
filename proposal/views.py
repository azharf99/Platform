import requests
from django.conf import settings
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from proposal.forms import ProposalForm, ProposalEditForm, StatusProposalForm, StatusProposalKepsekForm, StatusProposalBendaharaForm
from proposal.models import Proposal, ProposalStatus, ProposalStatusBendahara, ProposalStatusKepsek
from userlog.models import UserLog


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
                    message="Berhasil menambahkan data proposal {} dengan anggaran sebesar {} dan penanggung jawab {}".format(p.nama_event, p.anggaran_biaya, p.penanggungjawab)
                )

                url = 'https://api.watsap.id/send-message'
                headers = {'Content-Type': 'application/json'}
                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    'no_hp': '0%s' % request.user.teacher.no_hp,
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, berhasil mengajukan proposal *%s* dengan anggaran dana *%s* dan penanggung jawab *%s*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, p.nama_event, p.anggaran_biaya, p.penanggungjawab)
                }
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    # 'no_hp': '081293034867',
                    'no_hp': '085701570100',
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Ada mengajukan proposal baru yang masuk dengan rincian

*Nama proposal : %s*
*Anggaran dana : %s*
*Penanggung jawab : %s.*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.
https://ekskul.smasitalbinaa.com/proposal/approval/%s
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % ("Ustadz Panji Asmara, S.Pd.", p.nama_event, p.anggaran_biaya, p.penanggungjawab, p.id)
                }
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)
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
                message="Berhasil mengubah data proposal {}".format(data)
            )
            return redirect('proposal:proposal-index')
        else:
            forms = ProposalForm(instance=data)
            messages.error(request, "Data yang kamu isi ada yang salah. Silahkan periksa lagi.")
    else:
        forms = ProposalEditForm(instance=data)

    context = {
        'forms': forms,
    }

    return render(request, 'proposal-edit.html', context)

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
            message="Berhasil menghapus data proposal {}".format(data)
        )
        data.delete()
        return redirect('proposal:proposal-index')

    context = {
        'data': data,
    }
    return render(request, 'proposal-delete.html', context)


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
                message="Wakasek berhasil melakukan approval pada proposal {} dengan status {}".format(status, data.is_wakasek)
            )

            url = 'https://api.watsap.id/send-message'
            data_post = {
                'id_device': settings.ID_DEVICE,
                'api-key': settings.API_KEY,
                'no_hp': '0%s' % request.user.teacher.no_hp,
                'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, berhasil melakukan approval proposal *%s* dengan status *%s* dan komentar *%s*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, status.nama_event, data.is_wakasek, data.alasan_wakasek)
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

            data_post = {
                'id_device': settings.ID_DEVICE,
                'api-key': settings.API_KEY,
                # 'no_hp': '081398176123',
                'no_hp': '085701570100',
                'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Ada proposal baru yang masuk dengan rincian:

*Nama proposal : %s*
*Anggaran dana : %s*
*Penanggung jawab : %s.*
*Keputusan Wakasek saat ini: %s*
*Komentar dari Wakasek: %s*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.
https://ekskul.smasitalbinaa.com/proposal/approval/kepsek/%s
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % ("Ustadz Agung Wahyu Adhy, Lc.", status.nama_event, status.anggaran_biaya, status.penanggungjawab, data.is_wakasek, data.alasan_wakasek, status.id)
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

            data_post = {
                'id_device': settings.ID_DEVICE,
                'api-key': settings.API_KEY,
                # 'no_hp': '0%s' % status.penanggungjawab.no_hp,
                'no_hp': '085701570100',
                'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Proposal anda dengan judul *%s* telah *ditinjau oleh Wakasek Ekstrakurikuler*.
Mohon sekiranya Anda dapat meninjau status proposal tersebut pada aplikasi.
https://ekskul.smasitalbinaa.com/proposal
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (status.penanggungjawab, status.nama_event)
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)
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
    return render(request, 'proposal-approval.html', context)
@login_required(login_url='/login/')
def proposal_approval_kepsek(request, pk):
    if not request.user.username == "agung_wa":
        return redirect('restricted')
    status = Proposal.objects.get(id=pk)
    data = ProposalStatusKepsek.objects.get(proposal=status.id)
    if request.method == "POST":
        if data.status_wakasek.is_wakasek == "Accepted":
            forms = StatusProposalKepsekForm(request.POST, request.FILES, instance=data)
            if forms.is_valid():
                forms.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="APPROVAL",
                    app="PROPOSAL_KEPSEK",
                    message="Kepala Sekolah berhasil melakukan approval pada proposal {} dengan status {}".format(status, data.is_kepsek)
                )

                url = 'https://api.watsap.id/send-message'
                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    'no_hp': '0%s' % request.user.teacher.no_hp,
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, berhasil melakukan approval proposal *%s* dengan status *%s* dan komentar *%s*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, status.nama_event, data.is_kepsek, data.alasan_kepsek)
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    # 'no_hp': '085295188663',
                    'no_hp': '085701570100',
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Ada mengajukan proposal baru yang masuk dengan rincian:

*Nama proposal : %s*
*Anggaran dana : %s*
*Penanggung jawab : %s.*
*Keputusan Wakasek saat ini: %s*
*Komentar dari Wakasek: %s*
*Keputusan Kepala Sekolah saat ini: %s*
*Komentar dari Kepala Sekolah: %s*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.
https://ekskul.smasitalbinaa.com/proposal/approval/bendahara/%s
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % ("Ustadz Chevi Indrayadi, S.Si", status.nama_event, status.anggaran_biaya, status.penanggungjawab,
                    data.status_wakasek.is_wakasek, data.status_wakasek.alasan_wakasek, data.is_kepsek, data.alasan_kepsek, status.id)
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    # 'no_hp': '0%s' % status.penanggungjawab.no_hp,
                    'no_hp': '085701570100',
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Proposal anda dengan judul *%s* telah *ditinjau oleh Wakasek dan Kepala Sekolah*.
Mohon sekiranya Anda dapat meninjau status proposal tersebut pada aplikasi.
https://ekskul.smasitalbinaa.com/proposal
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (status.penanggungjawab, status.nama_event)
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)
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
                    message="Bendahara berhasil melakukan approval pada proposal {} dengan status {}".format(status, data.is_bendahara)
                )

                url = 'https://api.watsap.id/send-message'
                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    'no_hp': '0%s' % request.user.teacher.no_hp,
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum Ustadz %s, berhasil melakukan approval proposal *%s* dengan status *%s* dan komentar *%s*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, status.nama_event, data.is_bendahara, data.alasan_bendahara)
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

                data_post = {
                    'id_device': settings.ID_DEVICE,
                    'api-key': settings.API_KEY,
                    # 'no_hp': '0%s' % status.penanggungjawab.no_hp,
                    'no_hp': '085701570100',
                    'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Proposal anda dengan judul *%s* telah *ditinjau oleh Wakasek, Kepala Sekolah dan Bendahara*.
Mohon sekiranya Anda dapat meninjau status proposal tersebut pada aplikasi.

https://ekskul.smasitalbinaa.com/proposal

Bukti transfer dana (jika sudah ada):
https://ekskul.smasitalbinaa.com/proposal/approval/transfer/%s

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (status.penanggungjawab, status.nama_event, status.id)
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

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


def proposal_bukti_transfer(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    context = {
        'proposal': proposal,
    }
    return render(request, 'proposal-approval-transfer.html', context)