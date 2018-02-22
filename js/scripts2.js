
let fire = document.querySelector("#fire");
let digits = document.querySelector("#meter-container");
let ssaver = document.querySelector("#screensaver");

let digit = document.querySelector("#digit");

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

var year = 2018;

var oldTime = 0;
var DELAY = 1500;

var yearIndex = 0;

function incYearIndex() {
  yearIndex += 1;
  if (yearIndex > 4) {
    yearIndex = 0;
  }
}

function setYear(y) {
  year = y;
  yearIndex = 0;
  oldTime = 0;
}

function animation(time) {
  if ((time - oldTime) > DELAY) {
    oldTime = time;
    if (yearIndex < 4) {
      digit.innerHTML = ("" + year).charAt(yearIndex);
    } else {
      digit.innerHTML = "";
    }
    incYearIndex();
  }

  window.requestAnimationFrame(animation);
}

window.requestAnimationFrame(animation);


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
              , function() { showDigits(); setYear(2018); }
              , function() { showDigits(); setYear(7055); }
              , function() { showDigits(); setYear(4863); }
              , function() { showDigits(); setYear(7405); }
              , function() { showFire(); }
              , function() { showDigits(); }
              , function() { showDigits(); setYear(5047); }
              , function() { showSSaver(); setYear(1989); }
              , function() { showDigits(); }
              , function() { showDigits(); setYear(1922); }
              , function() { showDigits(); } // Ungdommens
              , function() { showDigits(); setYear(5048); }
              , function() { showDigits(); setYear(2018); }
];





var animation_time = 5000;  // The time it takes for the meter to change value


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

  if (scene < 0) {
    scene = scenes.length - 1;
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
  if(e.keyCode == 39){
    incScene();
  }
  if(e.keyCode == 37) {
    decScene();
  }
});
