#! usr/bin/env python3 | coding=utf-8
import random, os, sys, time, platform, threading, queue, json, datetime
from time import strftime
from rich import print as cetak
from rich.tree import Tree as akar
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.columns import Columns

konsol = Console()
folder_skor = "data"
file_skor = os.path.join(folder_skor, "score.json")

sys.stdout.write('\x1b]2; QUIZ | Quiz Matematika By WahyuXD\x07')

#               <!--  COLOR  -->
Z = "\x1b[0;90m"     # Hitam
M = "\x1b[38;5;196m" # Merah
H = "\x1b[38;5;46m"  # Hijau
K = "\x1b[38;5;226m" # Kuning
B = "\x1b[38;5;44m"  # Biru
U = "\x1b[0;95m"     # Ungu
O = "\x1b[0;96m"     # Biru Muda
P = "\x1b[38;5;231m" # Putih
J = "\x1b[38;5;208m" # Jingga
A = "\x1b[38;5;248m" # Abu-Abu
N = '\x1b[0m'	# WARNA MATI
PT = '\x1b[1;97m' # PUTIH TEBAL
MT = '\x1b[1;91m' # MERAH TEBAL
HT = '\x1b[1;92m' # HIJAU TEBAL
KT = '\x1b[1;93m' # KUNING TEBAL
BT = '\x1b[1;94m' # BIRU TEBAL
UT = '\x1b[1;95m' # UNGU TEBAL
OT = '\x1b[1;96m' # BIRU MUDA TEBAL

#                 <!-- Color 2  -->
Z2 = "[#ff0505]" # HITAM
mera  = "[#f00000]"
M2 = "[#AAAAAA]" # MERAH
H2 = "[#00FF00]" # HIJAU
K2 = "[#FFFF00]" # KUNING
B2 = "[#2400f5]" # BIRU
U2 = "[#AF00FF]" # UNGU
N2 = "[#FF00FF]" # PINK
O2 = "[#00FFFF]" # BIRU MUDA
P2 = "[#FFFFFF]" # PUTIH
J2 = "[#FF8F00]" # JINGGA
A2 = "[#AAAAAA]" # ABU-ABU
M2, H2, K2, P2, B2, U2, O2 = ["[#FF0000]", "[#00FF00]", "[#FFFF00]", "[#FFFFFF]", "[#2500ff]", "[#AF00FF]", "[#00FFFF]"]
acak = [M2, H2, K2, B2, U2, O2, P2]
warna = random.choice(acak)
til =f"{mera}● {K2}● {H2}●"
ken = f'{mera}›{K2}›{H2}› '
tod = f' {H2}‹{K2}‹{mera}‹'

# ----> Date
FR = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
tgl = datetime.datetime.now().day
bln = FR[(str(datetime.datetime.now().month))]
thn = datetime.datetime.now().year
hari   = {'Sunday':'Sunday','Monday':'Monday','Tuesday':'Tuesday','Wednesday':'Wednesday','Thursday':'Thursday','Friday':'Friday','Saturday':'Saturday'}[str(datetime.datetime.now().strftime("%A"))]

def bersihkan_layar():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def input_dengan_timer(prompt, batas_waktu):
    hasil = queue.Queue()
    def tunggu_input():
        try:
            jawab = input(prompt)
            hasil.put(jawab)
        except Exception:
            hasil.put(None)
    thread = threading.Thread(target=tunggu_input)
    thread.daemon = True
    thread.start()
    try:
        return hasil.get(timeout=batas_waktu)
    except queue.Empty:
        return None

def banner():
  logo = f"""[bold white]{til}{H2}                                               {hari}, {tgl} {bln} {thn}{warna}
    _______       _____       ________        ___________               
    __  __ \___  ____(_)_________  __ \____  ___  /___  /______________ 
    _  / / /  / / /_  /__  ___/_  /_/ /_  / / /  __/_  __ \  __ \_  __ \.
    / /_/ // /_/ /_  / _(__  )_  ____/_  /_/ // /_ _  / / / /_/ /  / / /
    \___\_\.__,_/ /_/  /____/ /_/     _\__, / \__/ /_/ /_/\____//_/ /_/ 
                                      /____/
                                      """
  cetak(Panel(logo,title=f"{ken}{P2}Quiz by WahyuXD{tod}",width=80,style="bold #ffffff"))

def buat_pertanyaan(level):
    if level == "m":
        operasi = ['+', '-']
        angka1 = random.randint(1, 10)
        angka2 = random.randint(1, 10)
    elif level == "s":
        operasi = ['+', '-', '*']
        angka1 = random.randint(5, 20)
        angka2 = random.randint(5, 20)
    else:
        operasi = ['+', '-', '*', '/']
        angka1 = random.randint(10, 30)
        angka2 = random.randint(1, 10)

    op = random.choice(operasi)
    if op == '/':
        angka1 = angka1 * angka2
        soal = f"{angka1} / {angka2}"
        jawaban = angka1 // angka2
    else:
        soal = f"{angka1} {op} {angka2}"
        jawaban = eval(f"{angka1}{op}{angka2}")
    return soal, jawaban

def pilih_jumlah_soal():
    return IntPrompt.ask(f"[bold]{P2}[{H2}?{P2}] Berapa jumlah soal?", choices=["5", "10", "20", "50"])

def pilih_level():
    return Prompt.ask(f"[bold]{P2}[{H2}?{P2}] Pilih tingkat kesulitan(mudah/sedang/sulit)", choices=["m", "s", "s"])

def konfirmasi_timer(level):
    if level == "s":
        return True
    pakai = Prompt.ask(f"[bold]{P2}[{H2}?{P2}] Mau pakai timer? (y/n)")
    return pakai == "y"

def simpan_skor(nama, skor, total):
    os.makedirs(folder_skor, exist_ok=True)
    data = []
    if os.path.exists(file_skor):
        with open(file_skor, 'r') as f:
            try:
                data = json.load(f)
            except:pass
    data.append({
        "nama": nama,
        "skor": skor,
        "total": total,
        "tanggal": tgl
    })
    with open(file_skor, 'w') as f:
        json.dump(data, f, indent=2)

def tampilkan_menu():
    m3nu = Panel.fit(f"[bold]{P2} Menu Utama ",style="bold #ffffff")
    m4nu = Panel.fit(f"[bold]{P2}Github: {H2}W4hyuXD{P2}",style="bold #ffffff")
    m5nu = Panel.fit(f"[bold]{P2}Version {H2}1.0{P2}",style="bold #ffffff")
    m6nu = Panel.fit(f"[bold]{P2}Instagram: {H2}@why.404_{P2}",style="bold #ffffff")
    columns = Columns([m3nu,m4nu,m5nu,m6nu])
    dalan = akar(columns, guide_style="bold #ffffff")
    dalan.add("1. Mulai Kuis")
    dalan.add("2. Lihat Skor Tersimpan")
    dalan.add("3. Putar Musik")
    dalan.add("4. Keluar")
    cetak(dalan)

def tampilkan_skor():
    bersihkan_layar()
    banner()
    if not os.path.exists(file_skor):
        cetak(f"[bold]{P2}[{M2}!{P2}]Belum ada skor tersimpan.")
    else:
        with open(file_skor, 'r') as f:
            data = json.load(f)
        if not data:
            cetak(f"[bold]{P2}[{M2}!{P2}]Belum ada skor tersimpan.")
        else:
            skor = Panel.fit(f"[bold]{P2}Riwayat Skor",style="bold #ffffff")
            for d in data[-10:]:
                tree = akar(skor,guide_style="bold #ffffff")
                tree.add(f"{d['tanggal']} - [cyan]{d['nama']}[/cyan]: {d['skor']} dari {d['total']}")
                cetak(tree)
    input("\n[!] Tekan ENTER untuk kembali ke menu...")

def putar_backsound(nama_file="musik.mp3"):
    try:
        os.popen(f"play-audio {nama_file}")
        cetak(f"{P2}[bold][{H2}✓{P2}] Musik diputar di latar belakang.")
    except:
        cetak(f"[bold]{P2}[{M2}!{P2}] Gagal memutar musik.")

def main_kuis():
    bersihkan_layar()
    banner()
    m3tu = Panel.fit(f"[bold]{P2}Input Name{P2}",style="bold #ffffff")
    metu = Panel.fit(f"[bold]{P2}Github: {H2}W4hyuXD{P2}",style="bold #ffffff")
    m1tu = Panel.fit(f"[bold]{P2}Version {H2}1.0{P2}",style="bold #ffffff")
    m2tu = Panel.fit(f"[bold]{P2}Instagram: {H2}@why.404_{P2}",style="bold #ffffff")
    columns = Columns([m3tu,metu,m1tu,m2tu])
    cetak(columns)
    nama = Prompt.ask(f"[bold]{P2}[{H2}+{P2}] Input Name")
    jumlah = pilih_jumlah_soal()
    level = pilih_level()
    pakai_timer = konfirmasi_timer(level)
    cetak(f"\n[bold]{P2}[{M2}!{P2}] Jika ingin mendengarkan musik latar, pastikan file 'musik.mp3' tersedia.")
    skor = 0
    salah_list = []
    for i in range(jumlah):
        bersihkan_layar()
        banner()
        soal1 = Panel.fit(f"[bold]{P2}Soal {H2}{i+1} {P2}dari {H2}{jumlah}",style="bold #ffffff")
        soal, jawaban = buat_pertanyaan(level)
        #cetak(f"[bold]{soal} = ?[/bold]")
        soale = akar(soal1,guide_style="bold #ffffff")
        soale.add(f"[bold][ {H2}{soal} {P2}= {K2}?{P2} ]")
        cetak(soale)
        if pakai_timer:
            jawab = input_dengan_timer("Jawab cepat (10s): ", 10)
            if jawab is None:
                cetak(f"\n[bold]{P2}[{M2}!{P2}] Waktu habis!")
                salah_list.append((soal, jawaban, "Waktu Habis"))
                continue
        else:
            jawab = input("\n[?] Jawabanmu: ")
        try:
            if int(jawab) == jawaban:
                cetak(f"\n[bold]{P2}[{H2}✓{P2}] Benar!")
                skor += 1
            else:
                cetak(f"\n[bold]{P2}[{M2}X{P2}] Salah! Jawaban: {jawaban}")
                salah_list.append((soal, jawaban, jawab))
        except:
            cetak(f"\n[bold]{P2}[{M2}!{P2}] Input tidak valid! Jawaban: {jawaban}")
            salah_list.append((soal, jawaban, jawab))
        time.sleep(1.5)

    bersihkan_layar()
    banner()
    cetak(Panel.fit(f"[bold cyan]Skor Akhir:{H2} {skor} {P2}dari {H2}{jumlah}[/bold cyan]"))
    simpan_skor(nama, skor, jumlah)

    if salah_list:
        cetak(f"[bold]{P2}[{K2}!{P2}] [red]Review Soal Salah: ")
        for s, jb, jp in salah_list:
            cetak(f"{H2}{s} {P2}= {H2}{jb} {P2}(jawabanmu:{M2} {jp}{P2})")
    input("\n[!] Tekan ENTER untuk kembali ke menu...")

def mulai():
    while True:
        bersihkan_layar()
        banner()
        tampilkan_menu()
        pilih = Prompt.ask(f"[bold]{P2}[{H2}?{P2}] Pilih opsi[/bold]")
        if pilih == "1":
            main_kuis()
        elif pilih == "2":
            tampilkan_skor()
        elif pilih == "3":
            putar_backsound()
            input("\n[!] Tekan ENTER untuk kembali...")
        elif pilih == "4":
            cetak("\n[bold][👋] Sampai jumpa![/bold]")
            break

if __name__ == "__main__":
    mulai()
