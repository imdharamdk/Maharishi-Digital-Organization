const themeToggle = document.getElementById('themeToggle');
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');
const filterButtons = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('#programCards .card');
const year = document.getElementById('year');
const volunteerForm = document.getElementById('volunteerForm');
const formNote = document.getElementById('formNote');

const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.body.classList.add('dark');
  themeToggle.textContent = '☀️';
}

themeToggle?.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  const isDark = document.body.classList.contains('dark');
  themeToggle.textContent = isDark ? '☀️' : '🌙';
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

menuToggle?.addEventListener('click', () => {
  navLinks.classList.toggle('show');
});

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    filterButtons.forEach((b) => b.classList.remove('active'));
    button.classList.add('active');
    const selected = button.dataset.filter;

    cards.forEach((card) => {
      const show = selected === 'all' || card.dataset.category === selected;
      card.style.display = show ? 'block' : 'none';
    });
  });
});

volunteerForm?.addEventListener('submit', () => {
  formNote.textContent = 'Thank you! Your volunteer form was submitted.';
});

year.textContent = new Date().getFullYear();
