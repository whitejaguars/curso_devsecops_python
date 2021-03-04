$(function () {
    if ($(window).width() > 450) {
      new WOW().init();
    }
    if (document.getElementById("particles-header")) particlesJS("particles-header", {"particles":{"number":{"value":7,"density":{"enable":true,"value_area":800}},"color":{"value":["#FFFFFF", "#FFFFFF", "#FFFFFF"]},"shape":{"type":"circle","stroke":{"width":0,"color":"#000000"},"polygon":{"nb_sides":6},"image":{"src":"img/github.svg","width":100,"height":100}},"opacity":{"value":0.15,"random":false,"anim":{"enable":false,"speed":1,"opacity_min":0.1,"sync":false}},"size":{"value":59.186073122420446,"random":true,"anim":{"enable":false,"speed":40,"size_min":0.1,"sync":false}},"line_linked":{"enable":false,"distance":0,"color":"#ffffff","opacity":0.4,"width":1},"move":{"enable":true,"speed":1,"direction":"top","random":false,"straight":false,"out_mode":"out","bounce":false,"attract":{"enable":false,"rotateX":157.82952832645452,"rotateY":1200}}},"interactivity":{"detect_on":"canvas","events":{"onhover":{"enable":false,"mode":"repulse"},"onclick":{"enable":false,"mode":"push"},"resize":true},"modes":{"grab":{"distance":400,"line_linked":{"opacity":1}},"bubble":{"distance":400,"size":40,"duration":2,"opacity":8,"speed":3},"repulse":{"distance":200,"duration":0.4},"push":{"particles_nb":4},"remove":{"particles_nb":2}}},"retina_detect":true});


    $(".filter-button").click(function(){
        var dataFilter = ["bundled","standards","sast","dast","it","mobile","software","plugins","trackers","tools","language"]
	    var filterValue = $(this).attr('data-filter');
	    $('.filter-button').removeClass('active');
	    $(this).addClass('active');
	    console.log(filterValue);

	    if(filterValue == "all"){
	        for(i=0; i<dataFilter.length; i++){
                $("."+dataFilter[i]).show(500);
            }
	    }else{
            for(i=0; i<dataFilter.length; i++){
                $("."+dataFilter[i]).hide(300);
            }
            $("."+filterValue).show(500);
	    }
	});
});
