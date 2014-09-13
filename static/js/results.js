$(document).ready(function() {
	var matches = $("#result_accordion h3");
	var auto_accordion;

	function switchMatches(arr){
	    var i = 1;
	    auto_accordion = setInterval(
	        function(){
	            arr[i].click();
	            i++;
	            if(i >= matches.length) i = 0;
	        },8000);
	}

	switchMatches(matches);

	$("#result_accordion h3").mouseup(function(ev) {
		clearInterval(auto_accordion);
		return true;
	});
});