var slider = document.getElementById("timeSlider");
var output = document.getElementById("sliderValue");
output.innerHTML = slider.value;

slider.oninput = function() {
    output.innerHTML = slider.value;
    var json = get_map_data();
    json.then(function(res) {
        var data = JSON.parse(res);
        var quarter_change = slider.value;
        var year = 2013;
        var quarter = 0;
        if (quarter_change % 4 == 0) {
            year = year + quarter_change / 4 - 1;
            quarter = quarter_change - (quarter_change / 4 - 1) * 4;
        } else {
            year = year + Math.floor(quarter_change / 4);
            quarter = quarter_change % 4;
        }
        var timecode = year * 10 + quarter;
        timecode = String(timecode);
        
        var year_data = data[timecode];
        console.log(year_data);
    });
}