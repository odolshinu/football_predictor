edit_prediction = function(prediction, score, home, away) {
	$("#prediction").val(prediction);
	$("#prediction_title").text(home+' vs '+away);
	$("#home_label").text(home);
	$("#away_label").text(away);
	var score_array = score.split('-');
	$("#current_home").val(score_array[0]);
	$("#current_away").val(score_array[1]);
	$('#edit_prediction').modal('show');
}