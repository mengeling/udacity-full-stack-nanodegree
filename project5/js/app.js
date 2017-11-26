// Declare global variables
var map;
var infoWindow;
var markers = [];


// This function initializes the map
function init() {

  // Create map object at central location
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 30.26, lng: -97.765},
    zoom: 13,
    mapTypeControlOptions: {position: google.maps.ControlPosition.TOP_RIGHT}
  });

  // Loop through parkMarkers and create a marker object each iteration
  for (var i=0; i < parkMarkers.length; i++) {

    // Create the marker object using the parkMarkers data
    var marker = new google.maps.Marker({
      map: map,
      id: parkMarkers[i].id,
      title: parkMarkers[i].title,
      position: parkMarkers[i].position,
    });

    // Add marker to empty markers array and create a click listener for it
    markers.push(marker);
    createClickListener(marker);

  }

  // Run application
  ko.applyBindings(new ViewModel());

}


// This function creates a click listener that opens an info window
function createClickListener(marker) {
  marker.addListener('click', function() {
    createInfoWindow(this);
  });
}


// This function creates an info window
function createInfoWindow(marker) {

  // If there's already an info window open, close it
  if (infoWindow) {
    infoWindow.close();
  }

  // Create Foursquare API url using the park's ID and client id and secret
  var apiUrl = 'https://api.foursquare.com/v2/venues/' + marker.id +
    '?client_id=ZCZJB4L2CNBDA0VYTEGDE0JFZACWBXC1S30LJ2MAOTRIG315&client_' +
    'secret=K52RW1KSIXMCOQ0HR15BZZFXYRWUP0MR2ZLAUPSX5YGDO5SD&v=20170911';

  // Get JSON data for the park's address, best photo, and foursquare URL
  $.getJSON(apiUrl, function(data) {
    var address = (
      data.response.venue.location.formattedAddress[0] + '<br>' +
      data.response.venue.location.formattedAddress[1]);
    var url = data.response.venue.canonicalUrl;
    var photo = (
      data.response.venue.bestPhoto.prefix + '120x160' +
      data.response.venue.bestPhoto.suffix);

    // Create info window variable for the selected marker
    infoWindow = new google.maps.InfoWindow({maxWidth: 120});
    infoWindow.marker = marker;

    // Set content to the marker's foursquare data
    infoWindow.setContent(
      '<img class="info-image" src="' + photo + '">' +
      '<div class="info-text">' + '<a target="_blank" href="' + url + '">' +
      marker.title + '</a>' + '<p>' + address + '</p>' +
      '<img src="img/foursquare.png" alt="Foursquare Logo" width="120"></div>');

    // Open the info window and add bounce animation
    infoWindow.open(map, marker);
    marker.setAnimation(google.maps.Animation.BOUNCE);

    // Stop animation after 2 bounces
    setTimeout(function() {
      marker.setAnimation(null);
    }, 1400);

  }).fail(function() {

    // If there's an error, create an info window and display an error message
    infoWindow = new google.maps.InfoWindow();
    infoWindow.marker = marker;
    infoWindow.setContent(
      'Sorry, an error occurred with Foursquare.<br>' +
      'Please look at the Console for details.');
    infoWindow.open(map, marker);

  });

}


// This function sets up the Knockout ViewModel
var ViewModel = function() {

  // Store ViewModel this in self variable
  var self = this;

  // Store search text in ko observable
  self.search = ko.observable('');

  // Create computed observable for the filtered parks
  // Return parks that have searched text in their name. Hide the other ones
  this.filteredParks = ko.computed(function() {
    return markers.filter(function(marker) {
      if (marker.title.toLowerCase().includes(self.search().toLowerCase())) {
        marker.setVisible(true);
        return marker;
      } else {
        marker.setVisible(false);
      }
    });
  }, this);


  self.mapSize = ko.computed(function() {
    if ($('aside').css('display') == 'none') {
      return '100%';
    } else {
      return 'calc(100% - 275px)';
    }
  });

};


// This function displays an error message in main if the map doesn't load
function mapError() {
  $('main').prepend(
    '<p class="map-error">Sorry, an error occurred with Google Maps. ' +
    'Please look at the Console for details.</p>');
}


// This function toggles the aside on and off the screen
function toggleAside() {

  // Toggle show-aside class on and off. Show-aside displays the aside as block
  $('aside').toggleClass('show-aside');

  // If aside is hidden move hamburger all the way to the right
  // Otherwise move the hamburger to the right of the aside
  if ($('aside').is(':hidden')) {
    $('.hamburger-container').css('margin-left', '0');
    // $('#map').css('width', '100%');
  } else {
    $('.hamburger-container').css('margin-left', '275px');
    // $('#map').css('width', 'calc(100% - 275px)');
  }

}
