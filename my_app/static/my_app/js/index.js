$(document).ready(function () {
  $(window).scroll(function () {
    if ($(this).scrollTop() > 10) {
      $(".plant-nav").css("background-color", "#1abc9c");
      $(".plant-nav__mid__menu a").css("color", "#fff");
      $(".plant-nav__right__menu a").css("color", "#fff");
    } else {
      $(".plant-nav").css("background-color", "transparent");
      $(".plant-nav__mid__menu a").css("color", "#000");
      $(".plant-nav__right__menu a").css("color", "#000");
    }
  });
});
