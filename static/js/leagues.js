launch_create_league_popup = function() {
	$("#create_league").popup("show");
}

launch_join_league_popup = function() {
	$("#join_league").popup("show");
}

group_settings = function(league, code, id) {
	$("#league_settings h1").text(league);
	$("#join_code").val(code);
	$("#league_settings").popup("show");
}