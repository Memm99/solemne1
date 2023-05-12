$(document).ready(function($) {
    
  
    Pace.on("done", function() {
        $(".pre_loader").css("display", "none");
    });
    

    $(".hero_title").each(function(i) {
            var $current_element = $(this);
            setTimeout(function() {
                $current_element.addClass("reveal");
            }, i * 100);
        });
  
    $("#rotating-text").Morphext({
    
    animation: "bounceIn",
    
    separator: ",",
    
    speed: 3000,
    complete: function () {
        
    }
});

       
     $('.owl-carousel').owlCarousel({
    items:1,
    loop:true,
    margin:0,
 

    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:false,
    animateOut: 'fadeOut'
     });
   
    
    
    
  
    
     $(".text_reveal:not(.in)").each(function(i) {
        var $current_element = $(this);
         $current_element.isInViewport(function(status) {
            if (status === "entered") {
                setTimeout(function() {
                    $current_element.addClass("in");
                }, i * 100);
            }
        });
    });

    $('.gallery').magnificPopup({
    delegate: 'a', //borrar
    type: 'image',
    gallery: {
        enabled: true
        
        }
    // other
    });

});

$(window).on("scroll", function() {
    if ($(window).scrollTop() > 0) {
        $(".navbar").addClass("nav-bg-black");
        $(".navbar:after").css("opacity","1");
        
    } else {
        $(".navbar").removeClass("nav-bg-black");

    }
});