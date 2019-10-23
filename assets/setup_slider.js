var slider = document.getElementById("timeSlider");

slider.oninput = function() {
    var slider = document.getElementById("timeSlider");
    var output = document.getElementById("sliderValue");
    var json = get_index_data();
    json.then(function(res) {
        var data = JSON.parse(res);
        var quarter_change = slider.value;
        var year = 2016;
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
        update_control(year_data);
    });
}