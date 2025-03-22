function toggleNav() {
    const topNav = document.querySelector('.top-nav');
    topNav.classList.toggle('active');
  }
  
  const hamburger = document.getElementById('hamburger');
  hamburger.addEventListener('click', toggleNav);
  