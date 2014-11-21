setInterval(function(){get_ajax();}, 5000);

function get_ajax(){
    var time = new Date().getTime();
    var time2 = new Date();
    time2.setSeconds(time2.getSeconds() - 5);
    document.getElementById('comments').innerHTML = document.getElementById('new_comments').innerHTML + document.getElementById('comments').innerHTML;
    document.getElementById('new_comments').innerHTML = "";
    $.ajax({
	    url: document.URL + "update/",
		type: "post",
		data: {"now": time2.getTime()},
		dataType: 'json',
		success: function(response) {
		var div = document.getElementById('new_comments');
		var json = response;
		for (key in json){
		    //var newli = document.createElement('li');
		    //newli.className = 'list-group-item';
		    div.innerHTML = '<li class="list-group-item">'+ json[key].content+'</li>' + div.innerHTML;
		    //<li class="list-group-item">{{comment.content}}</li>
		    //alert(json[key].content);
		}
	    }
	    
	});
}