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
        if (typeof(info._div) !== 'undefined') {
            var info_div = info._div;
            var p = (info_div.children)[1];
            var national_index = parseFloat((p.children)[0].innerHTML);
            reference = national_index;
        }
        else {
            reference=0;
        }
    }

    var retval =    d > reference ?     '#31a354':
                    d < reference ?     '#f03b20' :
                                        '#fec44f';
    return retval
                        
}

// How to color each province
function style(feature) {
    if (typeof feature.properties.index === 'undefined') {
        var data = get_food_data();

        data.then((res) => {
            var res = JSON.parse(res);
            var output = document.getElementById("sliderValue");
            var province_data = res[output.innerHTML][String(feature.properties.ID)];
            feature.properties.index = province_data['index'];
        });
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
    var province_json = get_food_data();
    province_json.then((food_province_json) => {
        var data = JSON.parse(food_province_json);
        var time_label = document.getElementById("sliderValue").innerHTML;
        var province_data = data[time_label][layer.feature.properties.ID];
        var commodities = Object.keys(province_data);

        var index = layer.feature.properties.index;
        if (typeof index !== 'undefined') {
            index = index.toFixed(2);
        }

        var popup_string = "Index: " + String(index) + "<br />";

        for (idx in commodities) {
            popup_string = popup_string + commodities[idx] + ": " + String(province_data[commodities[idx]].toFixed(2)) + "<br />";
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

function update_control(new_year_data){
    national_data = new_year_data['-1'];

    index_value = national_data['index'];
    info_string = '<h4>National Info</h4>' + (
        "<p>Indeks: <span>" + String(index_value.toFixed(2)) + "</span></p>"
    );

    for (variable in national_data) {
        if (variable == 'index') {
            continue;
        }
        info_string = info_string + `<p>${variable}: ${national_data[variable].toFixed(2)}</p>`;
    }

    info._div.innerHTML = info_string;
}

render_map(map);
render_control(map, info);