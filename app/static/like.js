$(document).ready(function() {
	// Set csrf so that server doesn't reject request
	var csrf_token = $('meta[name=csrf-token]').attr('content');
	 // Configure to that csrf is put at the header of every json file
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});
	
	$("a.like").on("click", function() {
		var clicked = $(this);
		var comment_id = $(this).attr("id");

		$.ajax({
			url: "/like",
			type: "POST",
			data: JSON.stringify({comment_id: comment_id}),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(response){
				console.log(response);
				console.log(clicked.children()[1].innerHTML);
				var newLiked = parseInt(clicked.children()[1].innerHTML) + response.amount;
				console.log(newLiked);
				clicked.children()[1].innerHTML = newLiked;
			},
			error: function(response){
				console.log(response);
			}
		});
	});
});