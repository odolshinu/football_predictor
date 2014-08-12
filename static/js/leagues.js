launch_create_league_popup = function() {
	$("#create_league").modal("show");
}

launch_join_league_popup = function() {
	$("#join_league").modal("show");
}

group_settings = function(league, code, id) {
	$("#settings_title").text(league);
	$("#join_code").val(code);
	$("#league_settings").modal("show");
}