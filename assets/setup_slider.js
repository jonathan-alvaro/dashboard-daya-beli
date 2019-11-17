var slider = document.getElementById("timeSlider");

function update_map() {
    var slider = document.getElementById("timeSlider");
    var output = document.getElementById("sliderValue");
    var json = get_food_data();
    json.then(function(res) {
        var data = JSON.parse(res);
        var quarter_change = slider.value;
        var year = 2017;
        var quarter = 0;
        if (quarter_change % 4 == 0) {
            year = year + quarter_change / 4 - 1;
            quarter = quarter_change - (quarter_change / 4 - 1) * 4;
        } else {
            year = year + Math.floor(quarter_change / 4);
            quarter = quarter_change % 4;
        }
        var timecode = String(year) + '-Q' + String(quarter);

        output.innerHTML = timecode;

        var year_data = data[timecode];
        update_national_column(year_data);

        geojson.eachLayer((layer) => {
            var id = layer.feature.properties.ID;
            layer.feature.properties.index = year_data[id]['index'];
        });

        geojson.setStyle((feature) => {
            var national_index = get_national_index_value();
            return {
                fillColor: getColor(feature.properties.index),
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            };
        });
        geojson.resetStyle();
    });
};

slider.oninput = update_map;
update_map();