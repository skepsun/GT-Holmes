maps = {
    initGoogleMaps: function(){
        var c = {lat: 33.7490, lng: -84.3880};
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 13,
            center: c,
            scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
            styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]
        });
        // var marker = new google.maps.Marker({
        //     position: uluru,
        //     map: map
        // });
        // var marker = new google.maps.Marker({
        //     position: c,
        //     icon: {
        //         path: google.maps.SymbolPath.CIRCLE,
        //         fillOpacity: 0.7,
        //         fillColor: rgbToHex(fcolor),
        //         //fillColor:[53, 0, 204],
        //         strokeOpacity: 1.0,
        //         strokeColor: '#fff000',
        //         strokeWeight: 1.0,
        //         scale: 10 //pixels
        //     }
        // });
        // marker.setMap(map);
    }

}
