1. Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.
   AuthenticationForm adalah form bawaan Django yang dipakai untuk proses login pengguna.
   Kelebihan:
   - Bawaan Django
   - Terintegrasi dengan sistem autentikasi Django
   - Sudah aman secara default, karena memvalidasi password dengan check_password(), mencegah login ke akun yang tidak aktif, dan it membocorkan detail apakah
     username atau password yang salah
   - Kompatibel dengan LoginView bawaan Django
   - Mudah dikustomisasi
   Kekurangan:
   - Terbatas pada username & password saja
   - Kurang fleksibel untuk tampilan UI
   - Tidak mendukung multi-step login
   - Tidak cocok untuk aplikasi dengan autentikasi modern (misalnya login via Google)

2.  Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?
   - Autentikasi (Authentication) -> proses memverifikasi identitas pengguna. Dengan user memasukkan username & password untuk memverifikasi apakah cocok dengan
     data
   - Otorisasi (Authorization) -> proses menentukan hak atau izin pengguna setelah identitasnya diverifikasi. Misalnya jika statusnya user, maka pengguna tidak bisa
     mengakses fitur yang hanya bisa diakses oleh admin.
     Django mengimplementasikan Authentication lewat django.contrib.auth, sedangkan Authorization diimplementasikan melalui decorator @login_required atau
     @permission_required('app.change_post') yang diletakkan diatas fungsi pada views.py

3.  Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?
    Session
    Kelebihan: Lebih aman, bisa simpan data kompleks, terintegrasi dengan login Django, mudah dikontrol server
    Kekurangan: Membebani server, butuh mekanisme cleanup, tidak bisa langsung diakses client-side
    Cookies
    Kelebihan: Ringan untuk server, mudah diakses client-side (JavaScript), dan persisten
    Kekurangan: Kurang aman, ukuran terbatas, terkirim di setiap request, rentan serangan seperti XSS atau cookie theft kalau tidak diamankan

4.  Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal
    tersebut?
    Tidak sepenuhnya aman, Cookies adalah data yang disimpan di sisi client (browser), jadi pengguna bisa melihat, mengubah, atau bahkan mencuri cookie kalau
    aplikasi tidak hati-hati. Resiko yang perlu diwaspadai adalah serangan-serangan seperti XSS (Cross-Site Scripting), Session Hijacking, CSRF (Cross-Site Request
    Forgery), dan Cookie Tampering. Dan cara Django untuk mengatasi serangan-serangan tersebut adalah dengan menggunakan session berbasis cookie, atribut keamanan
    cookie, CSRF Protection, dan signed cookies.

5.  Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
    - Mengimplementasikan fungsi registrasi
      Dengan cara membuat fungsi registrasi pada views.py dan membuat halaman html khusus registrasi
      def register(request):
         form = UserCreationForm()
    
   if request.method == "POST":
       form = UserCreationForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, 'Your account has been successfully created!')
           return redirect('main:login')
       context = {'form':form}
return render(request, 'register.html', context)

{% extends 'base.html' %}

{% block meta %}
<title>Register</title>
{% endblock meta %}

{% block content %}

<div>
  <h1>Register</h1>

  <form method="POST">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input type="submit" name="submit" value="Daftar" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

{% endblock content %}
 - Mengimplementasikan fungsi login
   Dengan cara membuat fungsi login pada views.py dan membuat halaman html khusus untuk login
   def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

   {% extends 'base.html' %}

   {% block meta %}
   <title>Login</title>
   {% endblock meta %}
   
   {% block content %}
   <div class="login">
     <h1>Login</h1>
   
     <form method="POST" action="">
       {% csrf_token %}
       <table>
         {{ form.as_table }}
         <tr>
           <td></td>
           <td><input class="btn login_btn" type="submit" value="Login" /></td>
         </tr>
       </table>
     </form>
   
     {% if messages %}
     <ul>
       {% for message in messages %}
       <li>{{ message }}</li>
       {% endfor %}
     </ul>
     {% endif %} Don't have an account yet?
     <a href="{% url 'main:register' %}">Register Now</a>
   </div>
   
   {% endblock content %}

   - Membuat fungsi logout
     Dengan menambahkan fungsi logout ke views.py dan tombol logout pada main.html
     def logout_user(request):
     logout(request)
     response = HttpResponseRedirect(reverse('main:login'))
     response.delete_cookie('last_login')
     return response

     <a href="{% url 'main:logout' %}" class="pill">Logout</a>

 -  Membuat dua (2) akun pengguna dengan masing-masing tiga (3) dummy data menggunakan model yang telah dibuat sebelumnya untuk setiap akun di lokal.
    Saya membuat 2 akun pengguna dengan masing-masing 3 dummy data pada lokal, lalu melihat hasilnya jika login di satu akun, maka produk yang dibuat oleh akun
    lain akan terlihat bahwa penjualnya berasal dari akun lain tersebut. begitu juga sebaliknya.
   
 -  Menghubungkan model Product dengan User.
    Dengan melakukan import from django.contrib.auth.models import User lalu menambahkan field user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

 -  Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last_login pada halaman utama aplikasi.
    Dengan menambahkan fitur last login pada bagian footer di base.html
    <p>Terakhir login: {{ last_login }}</p>
