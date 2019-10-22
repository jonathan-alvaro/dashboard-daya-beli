function get_map_data() {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        var data = '';

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