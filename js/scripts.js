$(document).ready(function(){

  let fire = document.querySelector("#fire");
  let digits = document.querySelector("#meter-container");
  let ssaver = document.querySelector("#screensaver");

  function showDigits() {
    digits.style.display = "block";
    fire.style.display = "none";
    ssaver.style.display = "none";
  }

  function showFire() {
    fire.style.display = "block";
    digits.style.display = "none";
    ssaver.style.display = "none";
  }

  function showSSaver() {
    ssaver.style.display = "block";
    fire.style.display = "none";
    digits.style.display = "none";
  }

  // Scenes: **************************8
  // Start
  // 2018 Tjoff presenterar maskinen
  // 7055 kaos
  // 4863 Boats and stuff
  // 7405 Åka fel
  // BRAND
  // 5047
  //
  // Paus
  //
  // 1989
  // 1922
  // Ungdommenskälla
  // 5048
  // 2018
  //
  let scenes = [  function() { showSSaver(); }
                , function() { showDigits(); }
                , function() { showDigits(); od.update(7055); }
                , function() { showDigits(); od.update(4863); }
                , function() { showDigits(); od.update(7405); }
                , function() { showFire(); }
                , function() { showDigits(); }
                , function() { showDigits(); od.update(5047); }
                , function() { showSSaver(); od.update(1989); }
                , function() { showDigits(); }
                , function() { showDigits(); od.update(1922); }
                , function() { showDigits(); } // Ungdommens
                , function() { showDigits(); od.update(5048); }
                , function() { showDigits(); od.update(2018); }
  ];





  var animation_time = 5000;  // The time it takes for the meter to change value
  var el = document.querySelector('#meter');

  od = new Odometer({
    el: el,
    value: 2018,
    minIntegerLen: 4,
    duration: 10000,
    format: 'dddd',
    //theme: 'digital',
  });

  var scene = 0;

  (scenes[scene])(); // Start first scene

  function incScene() {
    scene += 1;

    if (scene >= scenes.length) {
      scene = 0;
    }

    (scenes[scene])();
  }

  function decScene() {
    scene -= 1;

    if (scene > 0) {
      scene = scences.length;
    }

    (scenes[scene])();
  }

  // Server connection
  var c = new WebSocket('ws://localhost:8765');
  console.log(c);

  c.onmessage = function(e) {
    let a = (JSON.parse(e.data)).action;

    if (a === "Forward\r\n") {
      incScene();
    } else if (a === "Backward\r\n") {
      decScene();
    }
  }


  //var years = [2018, 7055, 5570, 4368, 7045, 5470, 1980, 1922, 0005, 2018];


  $('body').keydown(function(e) {
    if(e.keyCode == 32){
      incScene();
    }
    if(e.keyCode == 8) {
      decScene();
    }
  });
});
