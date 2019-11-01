var geojson;
var info = L.control();
var map = L.map('map', {
    minZoom: 5,
    maxZoom: 5,
    zoom: 5
});

// Function for color per province
function getColor(d, reference) {
    if (typeof(reference) === 'undefined') {
        reference = 210000;
    }
    var retval =    d > reference ?     '#31a354':
                    d < reference ?     '#f03b20' :
                                        '#fec44f';
    return retval
                        
}

// How to color each province
function style(feature) {
    if (typeof feature.properties.index === 'undefined') {
        feature.properties.index = (Math.random() * 3 + 20) * 10000;
    }
    return {
        fillColor: getColor(feature.properties.index),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// On hover styling
function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        dashArray: '',
        fillOpacity: 0.7
    })
    var province_json = get_province_food_data();
    province_json.then((food_province_json) => {
        var data = JSON.parse(food_province_json);
        var time_label = document.getElementById("sliderValue").innerHTML;
        var province_data = data[time_label][layer.feature.properties.ID];
        var commodities = Object.keys(province_data);

        var popup_string = "Index: " + String(layer.feature.properties.index) + "<br />";

        for (idx in commodities) {
            popup_string = popup_string + commodities[idx] + ": " + String(province_data[commodities[idx]]) + "<br />";
        }
        layer.bindPopup(popup_string).openPopup();
    });
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
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
        this._div.innerHTML = '<h4>National Info</h4>' + (
            '<p>Indeks 10 komoditas: <span>' + String(new_index) + '</span></p>'
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