document.addEventListener("DOMContentLoaded", function(){
  let showFeaturedOnly = false;
  let activeCategory = 'all';
  const grid = document.getElementById('grid');
  const q = document.getElementById('q');

  function updateView(){
    if(!grid) return;
    const cards = grid.querySelectorAll('.card');
    const query = q ? q.value.trim().toLowerCase() : '';
    cards.forEach(card=>{
      const cat = (card.dataset.category || '').toLowerCase();
      const featured = (card.dataset.featured === 'True' || card.dataset.featured === 'true' || card.dataset.featured === '1');
      const title = (card.querySelector('h3')?.textContent || '').toLowerCase();
      const desc = (card.querySelector('.desc')?.textContent || '').toLowerCase();

      let show = true;
      if(activeCategory !== 'all' && cat !== activeCategory.toLowerCase()) show = false;
      if(showFeaturedOnly && !featured) show = false;
      if(query && !(title.includes(query) || desc.includes(query))) show = false;

      card.style.display = show ? '' : 'none';
    });
  }

  // filter buttons (delegation)
  document.addEventListener('click', function(e){
    const t = e.target;
    if(t && t.matches('.filters .btn')){
      const btns = document.querySelectorAll('.filters .btn');
      btns.forEach(b=>b.classList.remove('active'));
      t.classList.add('active');
      activeCategory = t.dataset.cat || 'all';
      updateView();
    }
    if(t && t.id === 'featuredToggle'){
      showFeaturedOnly = !showFeaturedOnly;
      t.classList.toggle('btn-active');
      updateView();
    }
  });

  if(q){
    q.addEventListener('input', ()=>updateView());
  }

  // scroll helper used by CTA
  window.scrollToShop = function(){
    document.getElementById('shop')?.scrollIntoView({behavior:'smooth'});
  };

  // addToCart helper
  window.addToCart = function(name){
    alert('Menambahkan ke keranjang: ' + name);
  };

  // initial run
  updateView();
});
