




// $('document').ready(function(){
//     load_data()
// })



$(".post").click(function () {
    if ($("#firstname").val() == '' || $("#lastname").val() == ''|| tinymce.activeEditor.getContent() == '' || $("#title").val() == ''){
        $(".alert_container").html('')
        $(".alert_container").append('<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>Holy guacamole!</strong> You should check in on some of those fields below.<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
    }
    else{
        var d = new Date();
        var temp = {
            "username": $("#username").val(),
            "title":$("#title").val(),
            "time": d,
            "data": tinymce.activeEditor.getContent().replace(/"/gi,"<dquote>")
        }
        $.ajax({
            type: 'POST',
            crossDomain: true,
            url: '/post_content',
            contentType: "text/plain",
            data: JSON.stringify(temp),
            success: function (jsondata) {
                $(".alert_container").html('')
                $(".alert_container").append('<div class="alert alert-success alert-dismissible fade show" role="alert"><strong>Posted!</strong> Check your post below!<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
                console.log(jsondata)
                // load_data()
                clear();
            }
        });
    }

    
})


function clear(){
    tinymce.activeEditor.setContent('')
    $("input").val('')
}



