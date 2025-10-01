1. Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!
   Jika terdapat beberapa CSS selector untuk suatu elemen HTML, urutan prioritas CSS selectornya adalah:
   1. !important -> apapun selector yang memiliki penanda !important akan paling diprioritaskan.
   2. ID selector (#id) -> Lebih kuat daripada class atau elemen.
   3. Class, attribute, pseudo-class selector (.class, [type="text"], :hover)
   4. Element dan pseudo-element selector (p, h1, ::before, ::after)
   Jika terdapat spesifisitas yang sama, maka yang ditulis paling akhir yang akan dipakai.

2. Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design,
   serta jelaskan mengapa!
   Responsive design menjadi konsep yang penting dalam pengembangan aplikasi web karena membuat web menjadi fleksibel untuk diakses berbagai user dari perangkat yang
   berbeda. Terlebih lagi, sekarang banyak orang yang mengunjungi website menggunakan smartphone, oleh karena itu penyesuaian design web terhadap smartphone menjadi
   penting supaya user nyaman dalam mengakses web. Contoh aplikasi web yang sudah menerapkan responsive design adalah instagram, sedangkan yang belum menerapkan
   responsive design biasanya adalah website lama instansi pemerintah atau sekolah karena masih dibangun dengan layout fixed.

3. Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!
   Margin adalah jarak diluar border elemen yang berguna untuk memberi ruang antar elemen. Border adalah garis tepi yang mengelilingi padding dan content dan bisa
   style dengan diberi warna, ketebalan, dan gaya. Sedangkan Padding adalah jarak antara content dan border di dalam elemen yang berguna untuk memberi ruang pada
   teks atau gambar supaya tidak menempel ke border. Implementasinya:
   <!DOCTYPE html>
   <html>
   <head>
   <style>
   .box {
     margin: 20px;             
     border: 3px solid blue;    
     padding: 15px;             
     background-color: lightyellow;
   }
   </style>
   </head>
   <body>
   
   <div class="box">
     Ini adalah contoh box dengan <b>margin, border, padding</b>.
   </div>
   
   <div class="box">
     Kotak kedua, diberi jarak karena ada margin.
   </div>
   
   </body>
   </html>

4.  Jelaskan konsep flex box dan grid layout beserta kegunaannya!
    Flexbox dan grid layout adalah konsep yang digunakan untuk mengatur layout konten web. Bedanya flexbox digunakan untuk mengatur elemen layout 1 dimensi (baris
    atau kolom), sedangkan grid layout digunakan untuk mengatur elemen layout 2 dimensi (baris dan kolom).

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!
   - Untuk implementasi fungsi menghapus dan mengedit produk, saya menambahkan fungsi delete_product dan edit_product di views.py.
      def edit_product(request, id):
          product = get_object_or_404(Product, pk=id)
          form = ProductForm(request.POST or None, instance=product)
          if form.is_valid() and request.method == 'POST':
              form.save()
              return redirect('main:show_main')
      
          context = {
              'form': form
          }
      
          return render(request, "edit_product.html", context)
      
      def delete_product(request, id):
          product = get_object_or_404(Product, pk=id)
          product.delete()
          return HttpResponseRedirect(reverse('main:show_main'))
     Setelah menambah fungsi delete_product dan edit_product, saya import fungsi tersebut di urls.py dan mendefisikan url pattern nya.
      path('product/<uuid:id>/edit', edit_product, name='edit_product'),
      path('product/<uuid:id>/delete', delete_product, name='delete_product'),
   - Untuk kustomisasi design web, saya menggunakan CSS untuk syling design web nya.
