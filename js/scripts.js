$(document).ready(function(){

  var animation_time = 5000;  // The time it takes for the meter to change value
  var el = document.querySelector('.meter');

  var c = new WebSocket('ws://localhost:8765');
  console.log(c);

  c.onmessage = function(e) {
    let a = (JSON.parse(e.data)).action;

    if (a === "Forward\r\n") {
      i++;
      od.update(years[i]);
    } else if (a === "Backward\r\n") {
      i++;
      od.update(years[i]);
    }
  }

  od = new Odometer({
    el: el,
    value: 2018,
    minIntegerLen: 4,
    duration: 10000,
    format: 'dddd',
    theme: 'car',
  });

  var years = [2018, 7055, 5570, 4368, 7045, 5470, 1980, 1922, 0005, 2018];
  var i = 0;

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
