$(function () {
                $('#datetimepicker1').datetimepicker();
            });

$(document).ready(function() {
    $('#Carousel').carousel({
        interval: 5000
    })
});
$(document).ready(function() {
	$('.deliverable-infos').hide();
	$('.dropdown-deliverable').on('click', function(e) {
			console.log("dropdown toggled!");
			e.preventDefault();
			e.stopPropagation();
			//get targeted element via data-for attribute
			var dataFor = $(this).data('for');
			var idFor = $(dataFor);
			idFor.slideToggle();
	}); 
});
function initGoogleMap()
	{
		var myLatlng = new google.maps.LatLng(-1.177461,36.930013);
    	var mapOptions = 
    	{
    		center: myLatlng,
	       	zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			draggable: true,
			scrollwheel: false,
			zoomControl: true,
			zoomControlOptions:
			{
				position: google.maps.ControlPosition.RIGHT_CENTER
			},
			mapTypeControl: false,
			scaleControl: false,
			streetViewControl: false,
			rotateControl: false,
			fullscreenControl: true,
			styles:
			[
			  {
			    "featureType": "road.highway",
			    "elementType": "geometry.fill",
			    "stylers": [
			      {
			        "color": "#ffeba1"
			      }
			    ]
			  }
			]
    	}

    	// Initialize a map with options
    	map = new google.maps.Map(document.getElementById('map'), mapOptions);

		// Re-center map after window resize
		google.maps.event.addDomListener(window, 'resize', function()
		{
			setTimeout(function()
			{
				google.maps.event.trigger(map, "resize");
				map.setCenter(myLatlng);
			}, 400);
		});
	}