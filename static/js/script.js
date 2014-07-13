$(document).ready(function () {
    $.ajax({
        crossDomain: true,
        type: 'GET',
        dataType: 'json',
        contentType: "application/javascript",
        async: false,
        url: "http://localhost:5000/1/1",
        error: function (request, textStatus, errorThrown) {
            console.log(errorThrown);
        },
        success: function (msg) {
            var opts = ['name', 'address', 'estimated']
            var geojson = Sheetsee.createGeoJSON(msg, opts)
            var template = "<h4>{{name}}<br/>Address: {{address}}<br/>Estimated wait time: {{estimated}}m</h4>"
            var map = Sheetsee.loadMap("map")
            Sheetsee.addTileLayer(map, 'jllord.iiplg6lj')
            Sheetsee.addMarkerLayer(geojson, map, template)
        }
    });
});
