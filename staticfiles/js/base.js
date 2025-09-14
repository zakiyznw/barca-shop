function scrollToShop(){
  document.getElementById('shop').scrollIntoView({behavior:'smooth'});
}

function toggleNav(){
  const nl = document.getElementById('navLinks');
  nl.style.display = (nl.style.display === 'flex') ? 'none' : 'flex';
  nl.style.flexDirection = 'column';
}
