// put your own JavaScript here
(function() {
    "use strict";

    var mainNav = document.getElementById('mainNav');
    var headerHeight = mainNav.clientHeight;
    var previousTop = 0;

    document.querySelector('#mainNav + *').style.paddingTop = headerHeight + 16 + 'px';

    document.addEventListener("scroll", function() {
        // Show the navbar when the page is scrolled up
        // var curWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        var currentTop = window.scrollY;
        var force = ((currentTop > previousTop) && (previousTop > 0));

        mainNav.classList.toggle('hidden', force);

        previousTop = currentTop;
    })

})();
