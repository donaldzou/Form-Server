function load_data() {
    $.ajax({
        type: "GET",
        crossDomain: true,
        url: '/load_data',
        dataType: "json",
        async:true,
        success: function (data) {
            console.log(data)
            $(".content").html('')
            for (var n = data.length - 1; n >= 0; n--) {
                $(".content").append('<div id="' + data[n]['id'] + '"><hr><h5>'+data[n]['title']+'</h5><p style="font-weight: 800; font-size:10px">' 
                + data[n]['username'] 
                + '</p><div class="comment">'+data[n]['data'].replace(/<dquote>/gi,'"')
                +'</div>' + "<p style='text-align:right; font-size:10px'>" + data[n]['time'] + 
                '</p><button type="button" class="btn btn-outline-info edit btn-sm" data-toggle="modal" data-target="#exampleModalCenter" style="margin-right: 10px">Edit</button><button type="button" class="btn btn-outline-danger delete btn-sm">Delete</button></div>')
            }
            delete_button();
            edit_button();
            clear()
        }
    })
}


function delete_button(){
    $(".delete").click(function(){
        var id = $(this).parent().attr('id')
        var temp = {
            "id":id
        }
        $.ajax({
            type: 'POST',
            crossDomain: true,
            url: 'delete_content',
            contentType: "text/plain",
            data: JSON.stringify(temp),
            success: function (jsondata) {
                console.log(jsondata)
                load_data()
            }
        });
    })
}

function edit_button(){
    $(".edit").click(function(){
        var id = $(this).parent().attr('id')
        $(".modal").attr('content_id',id)
        tinymce.get("edit_c").setContent($(this).parent().children(".comment").html());
        $(".modal_alert").html('')
    })
}


function save_edit(){
    var temp = {
        "id": $(".modal").attr('content_id'),
        "data":tinymce.get("edit_c").getContent().replace(/"/gi,"<dquote>")
    }
    $.ajax({
        type: 'POST',
        crossDomain: true,
        url: 'edit_content',
        contentType: "text/plain",
        data: JSON.stringify(temp),
        success: function (jsondata) {
            var status = jsondata.split('-')
            $(".modal_alert").append('<div class="alert alert-'+status[0]+' alert-dismissible fade show" role="alert"><strong>'+status[1]+'</strong> '+status[2]+'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
            if (status[0] != "danger"){
                load_data()
                setTimeout(function(){
                    $('#exampleModalCenter').modal('toggle')
                },800)
            }
            
        }
    });
}

load_data()