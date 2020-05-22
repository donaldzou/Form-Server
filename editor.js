
function load_data() {
    $.ajax({
        type: "GET",
        crossDomain: true,
        url: 'http://localhost:8000/data.json',
        dataType: "json",
        success: function (data) {
            $(".content").html('')
            for (var n = data.length - 1; n >= 0; n--) {
                $(".content").append('<div id="' + data[n]['id'] + '"><hr><h6>' + data[n]['firstname'] + ' ' + data[n]['lastname'] + '</h6>' + data[n]['data'] + "<p style='font-size:7px'>" + data[n]['time'] + "</p></div>")
            }
        }
    })
}

$('document').ready(function(){
    load_data()
})


$(".btn").click(function () {
    var d = new Date();
    var temp = {
        "firstname": $("#firstname").val(),
        "lastname": $("#lastname").val(),
        "time": d,
        "data": tinymce.activeEditor.getContent()
    }
    $.ajax({
        type: 'POST',
        crossDomain: true,
        url: 'http://localhost:7070/post_content',
        contentType: "text/plain",
        data: JSON.stringify(temp),
        success: function (jsondata) {
            console.log(jsondata)
            load_data()
        }
    });



})