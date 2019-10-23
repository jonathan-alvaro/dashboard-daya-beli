function getColor(d) {
    return d > 0.5 ?    '#31a354':
                        '#f03b20'
}

function style(feature) {
    if (typeof feature.properties.growth === 'undefined') {
        feature.properties.growth = Math.random();
    }
    return {
        fillColor: getColor(feature.properties.growth),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

var geojson;

function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        dashArray: '',
        fillOpacity: 0.7
    })
    layer.bindPopup("growth: " + String(layer.feature.properties.growth).substring(0, 4)).openPopup();
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
    e.target.closePopup();
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });
}

function render_map(){
    var map = L.map('map', {
        minZoom: 5,
        maxZoom: 5,
        zoom: 5
    });

    map.panTo(new L.LatLng(-5, 120));

    geojson = L.geoJSON(indonesia, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
};

render_map();