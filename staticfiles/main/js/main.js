let items = []; // data produk
const grid = document.getElementById('grid');
const q = document.getElementById('q');
let showFeaturedOnly = false;
let activeCategory = 'all';

// URL AJAX fetch
const jsonUrl = "/products/json_ajax/"; // sesuai urls.py

// Ambil produk dari server via AJAX
async function fetchProducts() {
  try {
    const response = await fetch(jsonUrl);
    const data = await response.json();
    items = data;
    updateView(); // render grid
  } catch (err) {
    console.error("Gagal mengambil produk:", err);
  }
}

// Format harga
function formatPrice(n){
  return 'Rp ' + n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// Escape single quote untuk HTML
function escapeHtml(s){ return s.replaceAll("'", "\\'"); }

// Render produk ke grid
function render(itemsToRender){
  grid.innerHTML = '';
  if(itemsToRender.length === 0){
    grid.innerHTML = '<div style="color:var(--muted);grid-column:1/-1;text-align:center;padding:40px">Tidak ada produk.</div>';
    return;
  }
  itemsToRender.forEach(it=>{
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML = `
      <div class="thumb" style="background-image:url(${it.thumbnail})">
        ${it.is_featured?'<div class="badge">UNGULAN</div>':''}
      </div>
      <h3>${it.name}</h3>
      <div class="meta">
        <div class="pill">${it.category}</div>
        <div class="price">${formatPrice(it.price)}</div>
      </div>
      <div class="card-footer">
        <div style="color:var(--muted);font-size:13px">⭐ ${it.rating} • Stok ${it.stock}</div>
        <a href="/product/${it.id}/" class="add">Lihat Produk</a>
      </div>
    `;
    grid.appendChild(card);
  });
}

// Filter kategori
function filterCat(e){
  const btns = document.querySelectorAll('.filters .btn');
  btns.forEach(b=>b.classList.remove('active'));
  e.target.classList.add('active');
  activeCategory = e.target.dataset.cat;
  updateView();
}

// Toggle produk unggulan
function toggleFeatured(){
  showFeaturedOnly = !showFeaturedOnly;
  document.getElementById('featuredToggle').classList.toggle('btn-active');
  updateView();
}

// Update view berdasarkan filter, pencarian, featured
function updateView(){
  const qv = q.value.trim().toLowerCase();
  const filtered = items.filter(it=>{
    if(activeCategory!=='all' && it.category!==activeCategory) return false;
    if(showFeaturedOnly && !it.is_featured) return false;
    if(qv && !(it.name.toLowerCase().includes(qv) || it.description.toLowerCase().includes(qv))) return false;
    return true;
  });
  render(filtered);
}

// Event input pencarian
q.addEventListener('input', ()=>updateView());

// Fungsi tambah ke keranjang
function addToCart(name){
  alert('Menambahkan ke keranjang: ' + name);
}

// Scroll ke shop
function scrollToShop(){
  document.getElementById('shop').scrollIntoView({behavior:'smooth'});
}

// Panggil fetch saat load page
fetchProducts();
