var geojson;
var map = L.map('map', {
    minZoom: 4.3,
    maxZoom: 4.3,
    zoom: 4.3,
    dragging: false
});

function get_national_index_value() {
    var national_index = document.getElementById("national-index");

    return national_index.innerHTML;
}

// Function for color per province
function getColor(d) {

    var national_index = get_national_index_value();

    var retval = '#fec44f';

    if (d > national_index) {
        retval = '#f03b20';
    } else if (d < national_index) {
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

function render_table() {
    var table_div = document.getElementById("feature-table");

    var table = document.createElement('table');
    table.setAttribute("id", "comparison-table");

    for (var i = 0; i < 2; i++) {
        var tr = table.insertRow();

        for (var j = 0; j < 3; j++) {
            var th = document.createElement('th');

            if (i % 2 == 0) {
                if (j % 3 == 2) {
                    th.innerHTML = 'Nasional';
                }
            }

            if (i % 2 == 1) {
                if (j % 3 == 2) {
                    th.id = 'national-index';
                }
            }

            tr.appendChild(th);
        }
    }

    for (var i = 0; i < 10; i++) {
        var tr = table.insertRow();

        for (var j = 0; j < 3; j++) {
            var td = tr.insertCell();
        }
    }

    var data = get_food_data();
    data.then((res) => {
        var api_data = JSON.parse(res);
        var time_data = api_data[Object.keys(api_data)[0]];
        var location_data = time_data[Object.keys(time_data)[0]];
        var commodities = Object.keys(location_data);
        commodities.splice(commodities.indexOf('index'), 1);

        for (var i = 2, row; row = table.rows[i]; i++) {
            var header_cell = row.cells[0];
            header_cell.innerHTML = commodities[i-2];
        }
    });

    table_div.appendChild(table);
}

function update_national_column(year_data) {
    var table = document.getElementById("comparison-table");
    var national_data = year_data["-1"];

    for (var i = 2, row; row = table.rows[i]; i++) {
        var row_header = row.cells[0];
        var national_val = national_data[row_header.innerHTML];
        row.cells[2].innerHTML = national_val.toFixed(2);
    }

    table.rows[1].cells[2].innerHTML = national_data['index'].toFixed(2);
}

function update_province_column(province_data, province_name) {
    var table = document.getElementById("comparison-table");

    for (var i = 2, row; row = table.rows[i]; i++) {
        var row_header = row.cells[0];
        var province_val = province_data[row_header.innerHTML];
        row.cells[1].innerHTML = province_val.toFixed(2);
    }

    table.rows[1].cells[1].innerHTML = province_data['index'].toFixed(2);
    table.rows[0].cells[1].innerHTML = province_name;
}

render_table();
render_map(map);

var legend = L.control({position: 'bottomleft'});
legend.onAdd = function() {
    this._div = L.DomUtil.create('div', 'mapLegend');
    var red_dot = document.createElement('span');
    red_dot.setAttribute('id', 'redDot');
    red_dot.classList.add('dot');
    var yellow_dot = document.createElement('span');
    yellow_dot.setAttribute('id', 'yellowDot');
    yellow_dot.classList.add('dot');
    var green_dot = document.createElement('span');
    green_dot.setAttribute('id', 'greenDot')
    green_dot.classList.add('dot');
    this._div.appendChild(red_dot);
    this._div.innerHTML += '> Index Nasional';
    this._div.appendChild(yellow_dot);
    this._div.innerHTML += '= Index Nasional';
    this._div.appendChild(green_dot);
    this._div.innerHTML += '< Index Nasional';
    return this._div;
}
legend.addTo(map);