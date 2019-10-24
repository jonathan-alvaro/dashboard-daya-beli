function get_map_data() {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.open("GET","http://localhost:4000/api",true);
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var json_string = xhr.response;
                resolve(json_string);
            }
        }
    });
}

function get_index_data() {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.open("GET","http://localhost:4000/index_data",true);
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var json_string = xhr.response;
                resolve(json_string);
            }
        }
    });
}

function get_province_food_data() {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.open("GET","http://localhost:4000/province_food",true);
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var json_string = xhr.response;
                resolve(json_string);
            }
        };
    });
}