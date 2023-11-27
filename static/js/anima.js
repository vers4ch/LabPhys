let pendulum;
let backgroundImage;
let plank, sensor;
let plankX, plankY;
let prevMouseX, prevMouseY;
let dMouseY;
let displayText = false;
let period;
let length;
let angle = 0;
let n;
let start = false;
let randomError = 0;

function preload() {
  backgroundImage = loadImage('static/img/pendMain.png');
  plank = loadImage('static/img/pendPlank.png');
  sensor = loadImage('static/img/pendSensor2.png');
  open24Font = loadFont('static/fonts/Open24D.ttf');
}

function setup() {
	let canvas = createCanvas(403.3, 550);
	canvas.parent('animation-container');
	pendulum = new Pendulum(width/6, 10);
	plankX = 0;
	plankY = 0;
	prevMouseX = mouseX;
	prevMouseY = mouseY;
	frameRate(60);
  
	let startButton = document.getElementById('start-button');
	startButton.addEventListener('click', function() {
	  // Проверка ограничений перед началом анимации
	  const lengthInput = parseFloat(document.getElementById('length-input').value);
	  const thetaInput = parseFloat(document.getElementById('theta-input').value);
  
	  if (lengthInput >= 0.05 && lengthInput <= 1.0 && thetaInput >= -30 && thetaInput <= 180) {
		console.clear()
		start = true;
		displayText = false;// чтобы таймер гас после нажатия кнопки пуск
		n = 0;
		pendulum.init();
	  } else {
		alert("Пожалуйста, введите корректные значения.");
	  }
	});
}
  

function draw() {
  image(backgroundImage, 0, 0, width, height);
  scale(3);
  pendulum.update();
  pendulum.display();
  let plankWidth = width/3;
  let plankHeight = plankWidth * 0.13333;
  let sensorHeight = plankWidth * 0.2666;
  image(plank, plankX, plankY, plankWidth, plankHeight);
  image(sensor, 0, 100, plankWidth, sensorHeight);

  if (displayText) {
	fill(255, 0, 0);
	noStroke();
	textSize(5);
	textFont(open24Font);
	text(period.toFixed(3), width*0.156, height*0.207);
  }
}

function mouseDragged() {
  dMouseY = mouseY - plankY;
  let deltaY = mouseY - prevMouseY;
  if (
	mouseY > 0 &&
	mouseY < 430-length*3 &&
	mouseY < 270 &&
	mouseX < 350
  ) {
	plankY += deltaY/3;
	prevMouseY = mouseY;
  }
}

class Pendulum {
  constructor(originX, originY) {
	this.origin = createVector(originX, originY);
	this.position = createVector();
	this.init();
  }

  init() {
	this.armLength = document.getElementById('length-input').value * 100;
	length = this.armLength;
	this.angle = radians(parseInt(document.getElementById('theta-input').value));
	this.angleVelocity = 0.0;
	this.angleAcceleration = 0.0;
	// this.dampingFactor = 0.996;
	this.dampingFactor = 1.0;
	this.airResistance = 0.0;
	this.gravity = 9.80665;

	// Генерируем случайное число в диапазоне от -0.1 до 0.1 (например)
	randomError = (Math.random() - 0.5) * 0.46; // Измените 0.2 на желаемую амплитуду погрешности
	// console.log(randomError);
  }

  update() {
	// console.log("y = ", this.position.y + plankY)
	//ПОМЕНЯТЬ НА КОЭФФИЦЕНТЫ
	if( this.position.y + plankY > 107 && 
		this.position.y + plankY < 120 &&
		this.angle>0.001){
			if(displayText == false){
				setTimeout(() => {
					displayText = true;
				}, period*1000/1.3);
			}
	}
	
	//ЗДЕСЬ ДОБАВИТЬ ПОГРЕШНОСТЬ


	const actualPeriod = (2 * Math.PI * Math.sqrt(this.armLength / this.gravity) + randomError) / 10.0;
	period = actualPeriod;

	const TIME_STEPS_PER_SECOND = 60;
	const timeStep = actualPeriod / TIME_STEPS_PER_SECOND;

	const gravityForce = (-1) * this.gravity / this.armLength * Math.sin(this.angle);
	const airResistanceForce = -this.angleVelocity * this.airResistance;

	this.angleAcceleration = (gravityForce + airResistanceForce) / timeStep;
	this.angleVelocity += this.angleAcceleration * timeStep;
	this.angleVelocity *= this.dampingFactor;
	this.angle += this.angleVelocity * timeStep;

	this.position = createVector(this.armLength * Math.sin(this.angle), this.armLength * Math.cos(this.angle));

	this.position.add(this.origin);
  }

  display() {
	stroke(0);
	strokeWeight(0.5);
	line(this.origin.x, this.origin.y + plankY, this.position.x, this.position.y + plankY);
	// console.log(this.position.x)
	fill(127);
	ellipse(this.position.x, this.position.y + plankY, 5, 5);
  }
}