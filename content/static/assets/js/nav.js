(function() {
  var autoScrollSectionAnimation = function() {
    $(".page-scroll").click(function(
      event
    ) {
      event.preventDefault();
      $("html,body").animate(
        { scrollTop: $(this.hash).offset().top - 45 },
        400
      );
    });
  };

  var addClassNavbar = function() {
    $(".nav-l").addClass("transition-nav");
    $(".navbar-collapse-light").addClass("responsive-collapse");
    $("#img-nav").attr("src", "assets/img/logo-negro.png");
    $(".navbar-dark-courses").addClass("navbar-darkgray");
    $(".navbar-collapse-dark").addClass("responsive-collapse-dark");
  };

  var removeClassNavbar = function() {
    $(".nav-l").removeClass("transition-nav");
    $(".navbar-collapse-light").removeClass("responsive-collapse");
    $("#img-nav").attr("src", "assets/img/logo-blanco.png");
    $(".navbar-dark-courses").removeClass("navbar-darkgray");
    $(".navbar-collapse-dark").removeClass("responsive-collapse-dark");
  };

  var transitionNavOnScrollAndResize = function() {
    $(window).on("scroll", function() {
      if ($(window).width() > 994) {
        if ($(this).scrollTop() > 50) {
          $(".nav-l").addClass("transition-nav");
          $("#img-nav").attr("src", "assets/img/logo-negro.png");
          $(".navbar-dark-courses").addClass("navbar-darkgray");
        } else {
          removeClassNavbar();
        }
      }
    });

    $(window).resize(function() {
      if ($(window).width() <= 994 || $(this).scrollTop() > 50) {
        addClassNavbar();
      } else {
        removeClassNavbar();
      }
    });
  };

  var fixHeight = function() {
    if ($(window).width() < 994 || $(this).scrollTop() > 50) {
      addClassNavbar();
    } else {
      removeClassNavbar();
    }
  };

  var navOnChargeWebsite = function() {
    fixHeight();
    $(window).resize(function() {
      fixHeight();
    });
    $(".navbar .navbar-toggler").on("click", function() {
      fixHeight();
    });

    $(".navbar-toggler, .overlay, a.page-scroll").on("click", function() {
      $(".mobileMenu, .overlay").toggleClass("open");
      $(".animated-icon1").toggleClass("open");
    });
  };

  $(function() {
    //LLamado
    navOnChargeWebsite();
    transitionNavOnScrollAndResize();
    autoScrollSectionAnimation();
  });
})();
