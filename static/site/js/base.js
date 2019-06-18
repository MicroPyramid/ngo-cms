jQuery(document).ready(function () {
  "use strict";
  /* Mobile Menu */
  jQuery(document).ready(function () {
    jQuery('header nav.site-navigation').meanmenu();
  });
  /* Flex Slider Teaser */
  jQuery(window).load(function () {
    jQuery('.flexslider').flexslider({
      animation: "fade",
      animationLoop: true,
      controlNav: "thumbnails",
      start: function (slider) {
        jQuery('.flexslider').removeClass('loading');
      }
    });
  });
  /* Featured News Slider */
  jQuery(window).load(function () {
    jQuery('.flexslider-news').flexslider({
      controlNav: false,
      directionNav: true,
      animationLoop: true,
      animation: "fade",
      useCSS: true,
      smoothHeight: true,
      slideshow: false,
      slideshowSpeed: 3000,
      pauseOnAction: true,
      touch: true,
      animationSpeed: 900
    });
  });
  /* Toggle for Events */
  jQuery(".event-address").click(function () {
    jQuery(".event-map").toggle();
  });
  jQuery(".bookplace").click(function () {
    jQuery(".book-your-place").toggle();
  });
  /* Stick the menu */
  jQuery(function () {
    // grab the initial top offset of the navigation 
    var sticky_navigation_offset_top = jQuery('#sticky_navigation').offset().top + 40;
    // our function that decides weather the navigation bar should have "fixed" css position or not.
    var sticky_navigation = function () {
      var scroll_top = jQuery(window).scrollTop(); // our current vertical position from the top
      // if we've scrolled more than the navigation, change its position to fixed to stick to top, otherwise change it back to relative
      if (scroll_top > sticky_navigation_offset_top) {
        jQuery('#sticky_navigation').stop(true).animate({
          'padding': '5px 0;',
          'min-height': '60px',
          'opacity': 0.99
        }, 500);
        jQuery('#sticky_navigation').css({
          'position': 'fixed',
          'top': 0,
          'left': 0
        });
      } else {
        jQuery('#sticky_navigation').stop(true).animate({
          'padding': '20px 0;',
          'min-height': '60px',
          'opacity': 1
        }, 100);
        jQuery('#sticky_navigation').css({
          'position': 'relative'
        });
      }
    };
    sticky_navigation();
    jQuery(window).scroll(function () {
      sticky_navigation();
    });
  });
  /* Parallax Scroll */
  jQuery(function () {
    /* main background image. moves against the direction of scroll*/
    jQuery('.item').scrollParallax({
      'speed': -0.1
    });
  });
  /* Tabs */
  jQuery('.panes div').hide();
  jQuery(".tabs a:first").addClass("selected");
  jQuery(".tabs_table").each(function () {
    jQuery(this).find('.panes div:first').show();
    jQuery(this).find('a:first').addClass("selected");
  });
  jQuery('.tabs a').click(function () {
    var which = jQuery(this).attr("rel");
    jQuery(this).parents(".tabs_table").find(".selected").removeClass("selected");
    jQuery(this).addClass("selected");
    jQuery(this).parents(".tabs_table").find(".panes").find("div").hide();
    jQuery(this).parents(".tabs_table").find(".panes").find("#" + which).fadeIn(800);
  });
  /* Toggle */
  jQuery(".toggle-content .expand-button").click(function () {
    jQuery(this).toggleClass('close').parent('div').find('.expand').slideToggle(250);
  });
});
$(function () {
  if ($.support.msie && $.support.version.substr(0, 1) < 7) {
    $('li').has('ul').mouseover(function () {
      $(this).children('ul').css('visibility', 'visible');
    }).mouseout(function () {
      $(this).children('ul').css('visibility', 'hidden');
    });
  }
});