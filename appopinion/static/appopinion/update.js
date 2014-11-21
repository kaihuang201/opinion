setInterval(function(){get_ajax();}, 5000);

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function get_ajax(){
    var csrftoken = getCookie('csrftoken');
    var time = new Date().getTime();
    var time2 = new Date();
    time2.setSeconds(time2.getSeconds() - 5);
    document.getElementById('comments').innerHTML = document.getElementById('new_comments').innerHTML + document.getElementById('comments').innerHTML;
    document.getElementById('new_comments').innerHTML = "";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $.ajax({
	    url: document.URL + "update/",
		type: "post",
		data: {"now": time2.getTime()},
		dataType: 'json',
		success: function(response) {
            var div = document.getElementById('new_comments');
            var json = response;
            for (key in json){
                
                if(key != 'auth'){
                    var list_item = '<li class="list-group-item"><div><p>' + json[key].content + '</p><p>'; 
                    if(json['auth'] == 1){
                        list_item = list_item + "<a href='#' class='vote' data-commentid='" + json[key].commentid + "'";
                        list_item += " data-up='1'><span class=" + '"glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> </a>';
                        list_item +=  ' <span class="badge" id="votecount'+ json[key].commentid +'">'+ json[key].vote + "</span>";
                        list_item += "<a href='#' class='vote' data-commentid='" + json[key].commentid + "'";
                        list_item +=  " data-up='0'> <span class=" + '"glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> </a>';
                    }else{
                        list_item +=  '<span class="badge" id="votecount'+ json[key].commentid +'">'+ json[key].vote + "</span> Please sign in to vote";
                    }
                    document.getElementById('new_comments').innerHTML = list_item + document.getElementById('new_comments').innerHTML;
                    $('#new_comments').hide();
                    $('#new_comments').fadeIn("slow");
                }
            }
	    }
	    
	});
}
