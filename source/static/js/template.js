$(document).ready(function(){
    
	//Homepage Slider
    var options = {
        nextButton: false,
        prevButton: false,
        pagination: true,
        animateStartingFrameIn: true,
        autoPlay: true,
        autoPlayDelay: 3000,
        preloader: true
    };
    
    var mySequence = $("#sequence").sequence(options).data("sequence");

    //Main menu Initialization
    mainMenu.init();

	//Products slider
	var produxtsSlider = $('.products-slider').bxSlider({
		slideWidth: $('.products-slider .shop-item').outerWidth()-20, //Gets slide width
		responsive: true,
		minSlides: 1,
		maxSlides: 4,
		slideMargin: 20,
		auto: true,
		autoHover: true,
		speed: 800,
		pager: true,
		controls: false
	});

	//Make Videos Responsive
	$(".video-wrapper").fitVids();

	//Initialize tooltips
	$('.show-tooltip').tooltip();

	//Contact Us Map
	if($('#contact-us-map').length > 0){ //Checks if there is a map element
		L.mapbox.accessToken = 'pk.eyJ1IjoiaW5mb2dyb2VwIiwiYSI6IldFS1EtNWcifQ.yP7Vs_fv7C-JHU-OZxB4vA';
		var map = L.mapbox.map('contact-us-map', 'infogroep.ki0pgp77').setView([50.821553, 4.395609000000007], 15);
		var marker = L.marker([50.821553, 4.395609000000007]);
		marker.addTo(map).bindPopup("<b>Infogroep</b><br/>Pleinlaan 2<br/>1050 Brussels</br>Belgium").openPopup();
		marker.on('click', function(e){
			window.open("https://www.google.be/maps/place/50°49'17.4%22N+4°23'44.1%22E/@50.821514,4.395578,19z");
		});

	}
	if($('#about-us-map').length > 0){ //Checks if there is a map element
		L.mapbox.accessToken = 'pk.eyJ1IjoiaW5mb2dyb2VwIiwiYSI6IldFS1EtNWcifQ.yP7Vs_fv7C-JHU-OZxB4vA';
		var map = L.mapbox.map('about-us-map', 'infogroep.ki0pgp77').setView([50.820768, 4.395173], 15);
		var marker = L.marker([50.820768, 4.395173]);
		marker.addTo(map).bindPopup("<b>Infogroep Bedrijvendag</b><br/>Pleinlaan 2<br/>1050 Brussels</br>Belgium").openPopup();
		marker.on('click', function(e){
			window.open("https://www.google.be/maps/place/50°49'14.8%22N+4°23'42.6%22E/@50.820768,4.395173,18z");
		});
	}


	$( window ).resize(function() {
		$('.col-footer:eq(0), .col-footer:eq(1)').css('height', '');
		var footerColHeight = Math.max($('.col-footer:eq(0)').height(), $('.col-footer:eq(1)').height()) + 'px';
		$('.col-footer:eq(0), .col-footer:eq(1)').css('height', footerColHeight);
	});
	$( window ).resize();

});