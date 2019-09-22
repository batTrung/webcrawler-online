	(function(A) {

	if (!Array.prototype.forEach)
		A.forEach = A.forEach || function(action, that) {
			for (var i = 0, l = this.length; i < l; i++)
				if (i in this)
					action.call(that, this[i], i, this);
			};

		})(Array.prototype);

		var
		mapObject,
		markers = [],
		markersData = {
			'Marker': [
			{
				type_point: 'Hotel',
				name: 'Ocean Paradise',
				location_latitude: 48.868993, 
				location_longitude: 2.321236,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/single-listing/gallery-6.jpg',
				rate: '4.5',
				name_point: 'Ocean Paradise',
				url_point: 'single-listing-one.html',
				review: '13 reviews'
			},
			{
				type_point: 'Travel',
				name: 'Lagon Theme Park',
				location_latitude: 48.859183,
				location_longitude: 2.354808,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/place-5.jpg',
				rate: '4',
				name_point: 'Lagon Theme Park',
				url_point: 'single-listing-one.html',
				review: '12 reviews'
			},
			{
				type_point: 'Restaurent',
				name: 'Genji Restaurent',
				location_latitude: 48.869893, 
				location_longitude: 2.342348,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/place-9.jpg',
				rate: '5',
				name_point: 'Genji Restaurent',
				url_point: 'single-listing-two.html',
				review: '11 reviews'
			},
			{
				type_point: 'Travel',
				name: 'Lagon Theme Park',
				location_latitude: 48.868642,
				location_longitude: 2.352245,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/place-5.jpg',
				rate: '3.5',
				name_point: 'Lagon Theme Park',
				url_point: 'single-listing-one.html',
				review: '10 reviews'
			},
			{
				type_point: 'Caffee',
				name: 'Cafe Intermezzo',
				location_latitude: 48.859370, 
				location_longitude: 2.294481,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/cafe.jpg',
				rate: '4.5',
				name_point: 'Cafe Intermezzo',
				url_point: 'single-listing-two.html',
				review: '9 reviews'
			},
			{
				type_point: 'Hotel',
				name: 'Four Seasons Resort',
				location_latitude: 48.839273,
				location_longitude: 2.335387,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/place-1.jpg',
				rate: '5',
				name_point: 'Four Seasons Resort',
				url_point: 'single-listing-one.html',
				review: '8 reviews'
			},
			
			{
				type_point: 'Hotel',
				name: 'The Straling',
				location_latitude: 48.869819, 
				location_longitude: 2.354507,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/places/place-11.jpg',
				rate: '4',
				name_point: 'The Straling',
				url_point: 'single-listing-one.html',
				review: '14 reviews'
			},
			{
				type_point: 'Event',
				name: 'Muay Live Show',
				location_latitude: 48.866880, 
				location_longitude: 2.289205,
				map_image_url: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/category/event/muay.jpg',
				rate: '4',
				name_point: 'Muay Live Show',
				url_point: 'single-listing-five.html',
				review: '15 reviews'
			}
			
			]

		};

			var mapOptions = {
				zoom: 14,
				center: new google.maps.LatLng(48.865633, 2.321236),
				mapTypeId: google.maps.MapTypeId.ROADMAP,

				mapTypeControl: false,
				mapTypeControlOptions: {
					style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
					position: google.maps.ControlPosition.LEFT_CENTER
				},
				panControl: false,
				panControlOptions: {
					position: google.maps.ControlPosition.TOP_RIGHT
				},
				zoomControl: true,
				zoomControlOptions: {
					position: google.maps.ControlPosition.RIGHT_BOTTOM
				},
				scrollwheel: false,
				scaleControl: false,
				scaleControlOptions: {
					position: google.maps.ControlPosition.TOP_LEFT
				},
				streetViewControl: true,
				streetViewControlOptions: {
					position: google.maps.ControlPosition.LEFT_TOP
				},
				styles: [
  {
    "featureType": "administrative",
    "elementType": "geometry",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]
			};
			var marker;
			mapObject = new google.maps.Map(document.getElementById('map_right_listing'), mapOptions);
			for (var key in markersData)
				markersData[key].forEach(function (item) {
					marker = new google.maps.Marker({
						position: new google.maps.LatLng(item.location_latitude, item.location_longitude),
						map: mapObject,
						icon: '/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/others/marker.png',
					});

					if ('undefined' === typeof markers[key])
						markers[key] = [];
					markers[key].push(marker);
					google.maps.event.addListener(marker, 'click', (function () {
				  closeInfoBox();
				  getInfoBox(item).open(mapObject, this);
				  mapObject.setCenter(new google.maps.LatLng(item.location_latitude, item.location_longitude));
				 }));

	});

	new MarkerClusterer(mapObject, markers[key]);
	
		function hideAllMarkers () {
			for (var key in markers)
				markers[key].forEach(function (marker) {
					marker.setMap(null);
				});
		};
	
	

		function closeInfoBox() {
			$('div.infoBox').remove();
		};

		function getInfoBox(item) {
			return new InfoBox({
				content:
				'<div class="marker_info" id="marker_info">' +
				'<img src="' + item.map_image_url + '" alt=""/>' +
				'<span>'+ 
					'<em>'+ item.type_point +'</em>' +
					'<h3><a href="'+item.url_point+'">'+ item.name_point +'</a></h3>' +
					'<span class="infobox_rate">'+ item.rate +'</span>' +
					'<span class="btn_infobox_reviews">'+ item.review +'</span>' +
					'</span>' +
				'</div>',
				disableAutoPan: false,
				maxWidth: 0,
				pixelOffset: new google.maps.Size(10, 92),
				closeBoxMargin: '',
				closeBoxURL: "/static/websites/demolion-coders_dsdgmailcom51c90e78-2a70-4b36-b5bc-b095b9b9b778/images/others/close_infobox.png",
				isHidden: false,
				alignBottom: true,
				pane: 'floatPane',
				enableEventPropagation: true
			});
		};
function onHtmlClick(location_type, key){
     google.maps.event.trigger(markers[location_type][key], "click");
}
