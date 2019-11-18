var geojson;
var map = L.map('map', {
    minZoom: 4,
    maxZoom: 4,
    zoom: 4
});

function get_national_index_value() {
    var table = document.getElementById("comparison-table");
    var national_index = table.rows[11].cells[2].innerHTML;

    return national_index;
}

// Function for color per province
function getColor(d) {

    var national_index = get_national_index_value();

    var retval = '#fec44f';

    if (d < national_index) {
        retval = '#f03b20';
    } else if (d > national_index) {
        retval = '#31a354';
    }
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
        update_province_column(province_data, layer.feature.properties.Propinsi);
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
    map.panTo(new L.LatLng(-5, 117.5));

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

function render_table() {
    var table_div = document.getElementById("feature-table");

    var table = document.createElement('table');
    table.setAttribute("id", "comparison-table");

    for (var i = 0; i < 12; i++) {
        var tr = table.insertRow();

        for (var j = 0; j < 3; j++) {
            var td = tr.insertCell();

            if (i == 0) {
                if (j == 1) {
                    td.appendChild(document.createTextNode('Provinsi'));
                } else if (j == 2) {
                    td.appendChild(document.createTextNode('Nasional'));
                }
            }
        }
    }

    var data = get_food_data();
    data.then((res) => {
        var api_data = JSON.parse(res);
        var time_data = api_data[Object.keys(api_data)[0]];
        var location_data = time_data[Object.keys(time_data)[0]];
        var commodities = Object.keys(location_data);

        for (var i = 1, row; row = table.rows[i]; i++) {
            var header_cell = row.cells[0];
            header_cell.innerHTML = commodities[i-1];
        }
    });

    table_div.appendChild(table);
}

function update_national_column(year_data) {
    var table = document.getElementById("comparison-table");
    var national_data = year_data["-1"];

    for (var i = 1, row; row = table.rows[i]; i++) {
        var row_header = row.cells[0];
        var national_val = national_data[row_header.innerHTML];
        row.cells[2].innerHTML = national_val.toFixed(2);
    }
}

function update_province_column(province_data, province_name) {
    var table = document.getElementById("comparison-table");

    table.rows[0].cells[0].innerHTML = province_name

    for (var i = 1, row; row = table.rows[i]; i++) {
        var row_header = row.cells[0];
        var province_val = province_data[row_header.innerHTML];
        row.cells[1].innerHTML = province_val.toFixed(2);
    }
}

function update_national_index() {
    var national_index = get_national_index_value();
    var index_text_div = document.getElementById("index-div");

    index_text_div.innerHTML = national_index.toFixed(2);
}

render_table();
render_map(map);