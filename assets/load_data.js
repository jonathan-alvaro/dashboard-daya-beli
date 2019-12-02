function get_food_data() {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.open("GET","http://localhost:4000/data/food",true);
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var json_string = xhr.response;
                resolve(json_string);
            }
        };
    });
}