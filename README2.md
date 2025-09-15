 1. Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
    Penggunaan data delivery dalam pengimplementasian platform diperlukan karena tanpa tanpa data delivery, platform hanya menjadi seperti web statis, tidak ada interaksi antara client dan server. Selain itu pada
    pengembangan platform di zaman modern ini praktek penyediaan konten secara dinamis untuk user, real-time data update, dan pertukaran data antar sistem sangat masif dilakukan. Dan hal ini tidak mungkin bisa
    dilakukan tanpa adanya data delivery.
 2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
    Tidak ada yang lebih baik, semuanya tergantung kebutuhan. XML lebih baik apabila data yang ditukar sangat kompleks dan sistem environment yang digunakan masih sistem lama. JSON lebih baik apabila data sederhana
    dan butuh interaksi yang cepat dan ringan. Alasan mengapa JSON lebih populer dibandingkan XML adalah karena syntax JSON lebih ringkas dibandingkan XML, jika XML perlu tag pembuka dan penutup di setiap objeknya,
    maka JSON cukup menggunakan key value yang dibungkus oleh curly braces. Selain itu syntax JSON lebih mudah dibaca dibandingkan XML sehingga parsing bisa dilakukan lebih cepat karena syntax nya lebih sederhana.
 3. Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?
    method is_valid() adalah method bawaan django yang berfungsi memvalidasi data yang dikirim dari form untuk mengecek apakah semua fields terisi dengan benar. Method ini dibutuhkan karena berfungsi sebagai
    validator agar memastikan data yang masuk ke database sudah benar dan bersih.
 4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
    csrf_token diperlukan saat membuat form di django server dapat mengecek apakah token valid dan sesuai dengan session user, jadi token hanya benar benar dibuat di situs kita yang bisa diproses server. Jika tidak
    ada csrf_token maka akan muncul error 403 forbidden (csrf verification failed), hal ini terjadi karena django secara default menolak form POST tanpa csrf token. Jika kita mematikan proteksi ini, penyerang dapat
    membuat form palsu dari situs lain yang mengirim request ke server kita seolah-olah request tersebut dari user.
 5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
    - menambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan
      Di views.py saya menambahkan 4 fungsi views baru dalam formal xml, json, dan versi filtered by id nya.
      def show_xml(request):
        product_list = Product.objects.all()
        xml_data = serializers.serialize("xml", product_list)
        return HttpResponse(xml_data, content_type="application/xml")

      def show_json(request):
          product_list = Product.objects.all()
          json_data = serializers.serialize("json", product_list)
          return HttpResponse(json_data, content_type="application/json")
      
      def show_xml_by_id(request, product_id):
          try:
              product_item = Product.objects.filter(pk=product_id)
              xml_data = serializers.serialize("xml", product_item)
              return HttpResponse(xml_data, content_type="application/xml")
          except Product.DoesNotExist:
              return HttpResponse(status=404)
      
      def show_json_by_id(request, product_id):
          try:
              product_item = Product.objects.get(pk=product_id)
              json_data = serializers.serialize("json", [product_item])
              return HttpResponse(json_data, content_type="application/json")
          except Product.DoesNotExist:
              return HttpResponse(status=404)
    - membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 1.
      Di urls.py, saya membuat routing URL berdasarkan masing-masing fungsi baru pada views tadi
      path("products/xml/", show_xml, name="show_xml"),
      path("products/json/", show_json, name="show_json"),
      path("products/xml/<str:product_id>/", show_xml_by_id, name="show_xml_by_id_products"),
      path("products/json/<str:product_id>/", show_json_by_id, name="show_json_by_id_products"),

    - membuat halaman yang menampilkan data objek model yang memiliki tombol "Add" yang akan redirect ke halaman form, serta tombol "Detail" pada setiap data objek model yang akan menampilkan halaman detail objek.
      Pada bagian section class controls, saya membuat tombol Add yang dipasangkan di pojok kanan web, dengan detail kode seperti ini:
      <section class="controls">
        <div class="filters">
          <button class="btn active" data-cat="all" onclick="filterCat(event)">Semua</button>
          <button class="btn" data-cat="Jersey" onclick="filterCat(event)">Jersey</button>
          <button class="btn" data-cat="Accessory" onclick="filterCat(event)">Aksesori</button>
          <button class="btn" data-cat="Shoes" onclick="filterCat(event)">Sepatu</button>
        </div>
        <div style="display:flex;gap:8px;align-items:center;margin-left:auto;">
          <div class="pill" id="featuredToggle" onclick="toggleFeatured()">Tampilkan Unggulan</div>
          <a href="{% url 'main:add_product' %}" class="pill">Tambah Produk</a>  -> tombol "Add" nya
        </div>
      </section>

      Saya juga menambahkan section class grid lalu di tiap masing masing grid produk terdapat tombol "Lihat Produk" untuk menampilkan detail dari tiap objek
      <section id="shop" style="margin-top:16px;">
        <div class="grid" id="grid">
          {% for product in product_list %}
          <article class="card" data-category="{{ product.category }}" data-featured="{{ product.is_featured }}">
            <div class="thumb" style="background-image:url('{{ product.thumbnail }}')">
              {% if product.is_featured %}
              <div class="badge">UNGULAN</div>
              {% endif %}
            </div>
            <h3>{{ product.name }}</h3>
            <div class="meta">
              <div class="pill">{{ product.category }}</div>
              <div class="price">Rp {{ product.price|intcomma }}</div>
            </div>
            <div class="card-footer">
              <div>⭐ {{ product.rating }} • Stok {{ product.stock }}</div>
              <a href="{% url 'main:show_product' product.id %}" class="add">Lihat Produk</a>   -> Bagian tombol untuk melihat detail produk
            </div>
          </article>
          {% empty %}
          <div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--muted);">
            Belum ada produk.
          </div>
          {% endfor %}
        </div>
      </section>
      
    - membuat halaman form untuk menambahkan objek model pada app sebelumnya.
      saya membuat dokumen html baru sebagai halaman form untuk menambahkan objek model dengan nama add_product.html, dengan implementasi seperti ini:
      {% block content %}
      <main class="container" style="margin-top:40px; max-width:600px;">
        <h2>Tambah Produk Baru</h2>
        <p>Isi form berikut untuk menambahkan produk ke Barca Shop.</p>
      
        <form method="POST" class="form" style="margin-top:20px;">
          {% csrf_token %}
          
          <div class="form-group">
            <label for="id_name">Nama Produk</label>
            {{ form.name }}
          </div>
      
          <div class="form-group">
            <label for="id_price">Harga</label>
            {{ form.price }}
          </div>
      
          <div class="form-group">
            <label for="id_stock">Stok</label>
            {{ form.stock }}
          </div>
      
          <div class="form-group">
            <label for="id_description">Deskripsi</label>
            {{ form.description }}
          </div>
      
          <div class="form-group">
            <label for="id_thumbnail">URL Thumbnail</label>
            {{ form.thumbnail }}
          </div>
      
          <div class="form-group">
            <label for="id_category">Kategori</label>
            {{ form.category }}
          </div>
      
          <div class="form-actions">
            <button type="submit" class="btn-submit">Tambah Produk</button>
            <a href="{% url 'main:show_main' %}" class="btn-cancel">Batal</a>
          </div>
        </form>
      </main>
      {% endblock content %}

    -  membuat halaman yang menampilkan detail dari setiap data objek model.
       saya juga membuat dokumen html baru untuk menampilkan detail dari setiap objek model melalui tombol "lihat produk"
      {% block content %}
      <main class="container" style="margin-top:40px; max-width:700px;">
        <img class="detail-thumb" src="{{ product.thumbnail }}" alt="{{ product.name }}">
        <h2>{{ product.name }}</h2>
        <p class="price">Rp {{ product.price|intcomma }}</p>
        <p class="meta">⭐ {{ product.rating }} • Stok {{ product.stock }}</p>
        <p style="margin-top:15px;">{{ product.description }}</p>
      
        <div class="detail-actions">
          <button class="add" onclick="addToCart('{{ product.name }}')">Add to Cart</button>
          <a href="{% url 'main:show_main' %}" class="btn-cancel">Home</a>
        </div>
      </main>
      {% endblock content %}
      
      {% block extra_js %}
      <script>![Uploading Screenshot 2025-09-16 051904.png…]()

      function addToCart(name){
        alert('Menambahkan ke keranjang: ' + name);
      }
      </script>
      {% endblock extra_js %}

Screenshots akses URL XML melalui postman
<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/de231a46-4afa-4d8c-a04a-78576e794802" />

Screenshots akses URL JSON melalui postman
<img width="1913" height="1022" alt="Screenshot 2025-09-16 051931" src="https://github.com/user-attachments/assets/b262673e-cb96-44c7-bedb-ce93c833bc4f" />

Screenshots akes URL produk dengan id tertentu dengan XML melalui postman
<img width="1919" height="1025" alt="Screenshot 2025-09-16 052018" src="https://github.com/user-attachments/assets/7c79ec5e-d8a7-462f-bac9-36b30c9f87cd" />

Screenshots akes URL produk dengan id tertentu dengan JSON melalui postman
<img width="1919" height="1023" alt="Screenshot 2025-09-16 052030" src="https://github.com/user-attachments/assets/b0636252-0e92-4152-83dd-22fd1d961514" />

Feedback untuk asisten dosen, semoga tugas selanjutnya lebih seru dan tiap asistensi bisa membimbing kami dengan lebih baik.
    
