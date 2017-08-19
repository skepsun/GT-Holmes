mapObj = null;

var createInfoWindow = function (marker, content) {
    var infoWindow    = new google.maps.InfoWindow({});
        // contentString = String.format("<div id='info_window'>{0}</div>", content);

    google.maps.event.addListener(marker, "click", function() {
        //when the infoWindow is open, close it an clear the contents
        if (content == infoWindow.getContent()) {
            infoWindow.close(mapObj, marker);
            infoWindow.setContent("");
        }
        //otherwise trigger mouseover to open the infoWindow
        else {
            infoWindow.setContent(content);
            infoWindow.open(mapObj, marker);
        }
    });
    
}

maps = {
    initGoogleMaps: function (domId) {
        var c = {lat: 33.7490, lng: -84.3880};
        mapObj = new google.maps.Map(document.getElementById(domId), {
            zoom: 14,
            center: c,
            scrollwheel: false //we disable de scroll over the map, it is a really annoing when you scroll through page
            // styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]
        });
    },
    createSimilarMarkers: function (points) {
        return _.map(points, function (point) {
            var marker = new google.maps.Marker({
                position: point["position"],
                map: mapObj,
                icon: {
                  path: google.maps.SymbolPath.CIRCLE,
                  fillOpacity: 0.7,
                  fillColor: point["color"],
                  strokeOpacity: 1.0,
                  strokeColor: point["color"],
                  strokeWeight: 1.0,
                  scale: point["weight"]
                }
            });
            // Create info window for the marker
            var datetime = new Date(point["date"]*1000);
            var infoWindowHtml = String.format('\
                <div class="span4 collapse-group"><h2>{0}</h2><p>{1}, {2}</p>\
                <p id="remarks_{0}" class="collapse">{3}</p>\
                <button class="button" data-toggle="collapse" data-target="#remarks_{0}">details</button></div>', 
                point["id"], point["label"], datetime.toString(), point["text"]);
            createInfoWindow(marker, infoWindowHtml);
            return marker;
        });
    },
    clearMarkers: function (markers) {
        _.map(markers, function (marker) {
            marker.setMap(null);
        });
    },
    showMarkers: function (markers) {
        _.map(markers, function (marker) {
            marker.setMap(mapObj);
        });
    }
}
