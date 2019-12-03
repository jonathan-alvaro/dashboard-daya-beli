var slider = document.getElementById("timeSlider");

function update_map() {
    var slider = document.getElementById("timeSlider");
    var output = document.getElementById("sliderValue");

    var months_since_start = parseInt(slider.value);
    var year = 2016;
    var month = 2;
    month = month + months_since_start;
    if (month > 12) {
        if (month % 12 != 0) {
            var year_diff = Math.trunc(month / 12);
            year = year + year_diff;
            month = month - (12 * year_diff);
        } else {
            var year_diff = month / 12 - 1;
            year = year + year_diff;
            month = month - (12 * year_diff);
        }
    }

    month_dict = {
        '1': 'JAN',
        '2': 'FEB',
        '3': 'MAR',
        '4': 'APR',
        '5': 'MEI',
        '6': 'JUN',
        '7': 'JUL',
        '8': 'AUG',
        '9': 'SEP',
        '10': 'OKT',
        '11': 'NOV',
        '12': 'DES'
    };

    var timecode = month_dict[String(month)]+ '-' + String(year);

    output.innerHTML = timecode;

    var json = get_food_data(year, month_dict[String(month)]);
    json.then(function(res) {
        var month_data = JSON.parse(res);
        update_national_column(month_data);

        geojson.eachLayer((layer) => {
            var id = layer.feature.properties.ID;
            layer.feature.properties.index = month_data[id]['index'];
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