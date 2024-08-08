document.addEventListener('DOMContentLoaded', function() {
    const homeBg = document.getElementById('home-bg');
    const images = [
        homeBg.getAttribute('data-img1'),
        homeBg.getAttribute('data-img2'),
        homeBg.getAttribute('data-img3')
    ];

    let currentIndex = 0;

    function changeBackground() {
        homeBg.style.backgroundImage = `url(${images[currentIndex]})`;
        currentIndex = (currentIndex + 1) % images.length;
    }

    setInterval(changeBackground, 2000);
    changeBackground(); // Initial call to set the first background image
});
