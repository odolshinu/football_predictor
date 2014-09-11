$(document).ready(function() {
	var matches = $("#result_accordion h3");

	function switchMatches(arr){
		console.log(arr);
	    var i = 1;
	    setInterval(
	        function(){
	            arr[i].click();
	            i++;
	            if(i >= matches.length) i = 0;
	        },8000);
	}

	switchMatches(matches);
});