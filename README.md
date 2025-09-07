1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
checklist 1 (membuat proyek django baru) -> saya membuat repository baru di github dan menghubungkannya di lokal, setelah itu saya mempersiapkan dependancy apa saja yang digunakan untuk memulai proyek django dengan requirements.txt, mengunggah repository ke github, lalu mendeploy lewat pws.
checklist 2 (Membuat aplikasi dengan nama main pada proyek tersebut) -> dengan membuat file urls.py lalu menamakan app_name = 'main'.
checklist 3 (Melakukan routing pada proyek agar dapat menjalankan aplikasi main) -> dengan menambahkan path('', include('main.urls')), pada urlpatterns di urls.py level projek
checklist 4 (Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib sebagai berikut.
name sebagai nama item dengan tipe CharField) -> dengan mengubah atribut di models.py
checklist 5 (Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat) -> dengan menggunakan git push pws master pada cmd.

2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
[ Client (Browser) ]
         │
         ▼
  HTTP Request (GET/POST, dll)
         │
         ▼
  urls.py  ──> mencocokkan URL dengan view yang sesuai
         │
         ▼
  views.py ──> berisi fungsi/kelas yang menangani logika request
         │
         ├── (opsional) Memanggil models.py untuk ambil/simpan data ke DB
         │
         ▼
  models.py ──> mendefinisikan struktur tabel & interaksi dengan database
         │
         ▼
  views.py ──> mengolah data & memilih template
         │
         ▼
  templates (HTML) ──> merender data menjadi halaman web
         │
         ▼
  HTTP Response (HTML dikirim ke browser)
         │
         ▼
[ Client (Browser) menampilkan halaman ]


3. Jelaskan peran settings.py dalam proyek Django!
   - Menentukan aplikasi apa saja yang dipakai dalam proyek.
   - Mengatur koneksi ke database yang digunakan.
   - Menentukan lokasi folder template (HTML).
   - Mengatur keamanan dan debugging
     
4. Bagaimana cara kerja migrasi database di Django?
  dengan mendefinisikan model, lalu make migrate dengan python manage.py makemigrations, setelah itu menjalankan migrate dengan python manage.py migrate
   
5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
  karena dukungan dokumentasinya dan komunitasnya jelas, relevan di industri, dan menyediakan semua kebutuhan dasar pengembangan web.
   
6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
  Menurut saya asisten dosen tutorial 1 yang saya kerjakan sebelumnya sudah melaksanakan tugasnya dengan baik.
