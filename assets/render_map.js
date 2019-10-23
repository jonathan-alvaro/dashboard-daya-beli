var geojson;
var info = L.control();
var map = L.map('map', {
    minZoom: 5,
    maxZoom: 5,
    zoom: 5
});

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

function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        dashArray: '',
        fillOpacity: 0.7
    })
    layer.bindPopup("growth: " + String(layer.feature.properties.growth).substring(0, 4)).openPopup();

    info.update(get_index_data());
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

function render_map(map){
    map.panTo(new L.LatLng(-5, 120));

    geojson = L.geoJSON(indonesia, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);

    return map
};

function render_control(map, info){

    info.onAdd = function(map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    }

    info.update = function (new_index) {
        console.log(new_index)
        this._div.innerHTML = '<h4>National Info</h4>' + (
            '<p>Indeks 10 komoditas: ' + String(new_index) + '</p>'
        );
    }

    info.addTo(map);

    return info
}

function update_control(new_val){
    info.update(new_val)
}

render_map(map);
render_control(map, info);