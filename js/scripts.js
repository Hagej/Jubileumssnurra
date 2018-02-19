$(document).ready(function(){

	var years = [2018, 7055, 5570, 4368, 7045, 5470, 1980, 1922, 0005, 2018];
	var i = 0;

	var animation_time = 5000; 	// The time it takes for the meter to change value
	var el = document.querySelector('.meter');

	od = new Odometer({
		el: el,
		value: 2018,
		minIntegerLen: 4,
		duration: 10000,
		format: 'dddd',
		theme: 'car',

	});

	var backgrounds = new Array(
		'url(../Jubileumsbakgrund1.svg)',
		'url(../Jubileumsbakgrund2.svg)',
		'url(../Jubileumsbakgrund3.svg)'
	);

	$('body').keydown(function(e) {
		if(e.keyCode == 32){
			i++;
			od.update(years[i]);
		}
		if(e.keyCode == 8) {
			i--;
			od.update(years[i]);
		}
	});
});