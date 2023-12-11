import requests
from django.conf import settings
token = settings.TOKEN            

def send_whatsapp_input_anggota(phone, data, judul, link, aksi):
    message = f'''*[NOTIFIKASI]*
Anda berhasil {aksi} {judul} *{data}*.
Detail:
https://pmbp.smasitalbinaa.com/{link}

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)

def send_whatsapp_login(phone, aksi, welcome):
    message = f'''*[NOTIFIKASI]*
Anda berhasil {aksi}.
{welcome}. Jika ada yang ditanyakan terkait aplikasi, silahkan hubungi:
https://wa.me/6285701570100

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_laporan(phone, data, *args):
    message = f'''*[NOTIFIKASI LAPORAN EKSKUL]*
Anda berhasil {args[0]} laporan pertemuan ekskul *{data.nama_ekskul}* untuk tanggal *{args[1]}*.
Detail laporan:
https://pmbp.smasitalbinaa.com/laporan/{data.slug}

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)

def send_whatsapp_laporan_osn(phone, bidang, *args):
    message = f'''*[NOTIFIKASI LAPORAN OSN]*
Anda berhasil {args[0]} laporan pertemuan OSN *{bidang}* untuk tanggal *{args[1]}*.
Detail laporan:
https://pmbp.smasitalbinaa.com/osn/{bidang.slug}

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_print(phone, *args):
    message = f'''*[NOTIFIKASI LAPORAN EKSKUL]*
Anda berhasil {args[0]} laporan pertemuan {args[1]} {args[2]}.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_proposal(phone, proposal, *args):
    message = f'''*[NOTIFIKASI]*
Anda berhasil {args[0]} proposal *{args[1]}* dengan anggaran dana *{proposal.anggaran_biaya}* dan penanggung jawab *{proposal.penanggungjawab}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)

def send_whatsapp_proposal_review(phone, judul_proposal, status):
    message = f'''*[NOTIFIKASI]*
Proposal anda dengan judul *{judul_proposal}* telah *ditinjau oleh Wakasek Ekstrakurikuler*.
Status Proposal : {status.is_wakasek}
Komentar Wakasek: {status.alasan_wakasek}
Mohon sekiranya Anda dapat meninjau status proposal tersebut pada aplikasi.
https://pmbp.smasitalbinaa.com/proposal

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_proposal_approval(phone, *args):
    message = f'''*[NOTIFIKASI]*
Anda berhasil melakukan approval proposal *{args[0]}* dengan status *{args[1]}* dan komentar *{args[2]}*.
Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_proposal_wakasek(phone, proposal, link='', *args):
    message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {args[0]}, ada proposal baru yang masuk dengan rincian:

*Nama proposal : {args[1]}*
*Anggaran dana : {proposal.anggaran_biaya}*
*Penanggung jawab : {proposal.penanggungjawab}*


Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.

*Link Approval:*
https://pmbp.smasitalbinaa.com/proposal{link}/approval/{proposal.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_proposal_kepsek(phone, proposal, status, link='', *args):
    message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {args[0]}, ada proposal baru yang masuk dengan rincian:

*Nama proposal : {args[1]}*
*Anggaran dana : {proposal.anggaran_biaya}*
*Penanggung jawab : {proposal.penanggungjawab}*
*Keputusan Wakasek saat ini: {status.is_wakasek}*
*Komentar dari Wakasek: {status.alasan_wakasek}*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.

Link Approval:
https://pmbp.smasitalbinaa.com/proposal{link}/approval/kepsek/{proposal.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)


def send_whatsapp_proposal_bendahara(phone, proposal, status, link='', *args):
    message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {args[0]}, Ada proposal baru yang masuk dengan rincian:

*Nama proposal : {args[1]}*
*Anggaran dana : {proposal.anggaran_biaya}*
*Penanggung jawab : {proposal.penanggungjawab}*

*Keputusan Wakasek saat ini: {status.status_wakasek.is_wakasek}*
*Komentar dari Wakasek: {status.status_wakasek.alasan_wakasek}*

*Keputusan Kepala Sekolah saat ini: {status.is_kepsek}*
*Komentar dari Kepala Sekolah: {status.alasan_kepsek}*

Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.

*Link Approval:*
https://pmbp.smasitalbinaa.com/proposal{link}/approval/bendahara/{proposal.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)



def send_whatsapp_proposal_finish(phone, proposal, link='', *args):
    message = f'''*[NOTIFIKASI]*
Assalamu'alaikum {args[0]}, Proposal *{args[1]}*
*Telah di-approve oleh Bendahara dan dana dikirim melalui nomer rekening Ustadz Panji atau PJ yang bersangkutan.*
Mohon sekiranya ustadz dapat meninjau proposal tersebut pada aplikasi.

Bukti transfer dana:
https://pmbp.smasitalbinaa.com/proposal{link}/approval/transfer/{proposal.id}

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._'''
    url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
    return requests.get(url)