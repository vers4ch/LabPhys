let backgroundImage;
let on = false;
let buttonOffImage, buttonOnImage;

let buttonX = 390;
let buttonY = 670;
let buttonWidth = 35;
let buttonHeight = 30;

let circleX = 420;
let circleY = 625;
let circleRadius = 20;

let arrowBaseX = 130;
let arrowBaseY = 604;
let arrowLength = 65;
let angleV0 = 0;

let AmperArrowBaseX = 305;
let AmperArrowBaseY = 603;
let AmperArrowLength = 65;
let AmperAngleV0 = 0;

let length = 0.3;
let voltageValue = 0;
let amperValue = 0;

let plankY = 15;
let prevMouseX = 0;
let prevMouseY = 0;

let mouseClickY = 0;

let currentVoltageAngle = 30;
let targetVoltageAngle = 30;

let currentAmperAngle = 30;
let targetAmperAngle = 30;

function preload() {
  backgroundImage = loadImage('static/img/asx.png');
  buttonOffImage = loadImage('static/img/buttonOff.png');
  buttonOnImage = loadImage('static/img/buttonOn.png');
  lampOnImage = loadImage('static/img/lampOn.png');
  begunImage = loadImage('static/img/h.png');
  open24Font = loadFont('static/fonts/Open24D.ttf');
}

function setup() {
	let canvas = createCanvas(480, 773);

    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

	canvas.parent('animation-container');


	plankY = 15;
	prevMouseX = mouseX;
	prevMouseY = mouseY;

    currentVoltageAngle = 32;
    currentAmperAngle = 31;
}

  

function draw() {
  image(backgroundImage, 0, 0, width, height, 0);
  prevMouseY = mouseY;
  image(begunImage, 0, plankY, width, width/9.8, 1);

  length = calculateLength();

  // Отображение соответствующего изображения в зависимости от переменной on
  if (on) {
    image(buttonOnImage, 0, 0, width, height, 1);
    image(lampOnImage, 0, 0, width, height, 1);
  } else {
    image(buttonOffImage, 0, 0, width, height, 1);
  }

  voltagenArrow();
  amperArrow();

  updateArrows();
  

  if (mouseX > buttonX && mouseX < buttonX + buttonWidth && mouseY > buttonY && mouseY < buttonY + buttonHeight) {
    cursor(HAND); // Изменение типа курсора на указатель (hand) при наведении на кнопку
  } else {
    cursor(ARROW); // Возвращение обычного типа курсора вне зоны кнопки
  }

}

function calculateLength() {
    // Заданные точки (plankY, length)
    const point1 = { x: 40, y: 0.5 };
    const point2 = { x: 455, y: 0 };
  
    // Линейная интерполяция
    const length = interpolate(plankY, point1.x, point1.y, point2.x, point2.y);
  
    return length;
}
  
function interpolate(x, x1, y1, x2, y2) {
    // Формула линейной интерполяции
    return y1 + ((x - x1) / (x2 - x1)) * (y2 - y1);
}



function mouseDragged() {
    let deltaY = mouseY - prevMouseY;
    if (
      mouseY > plankY - 100 &&
      mouseY < plankY + width/9.8 + 100 &&
      mouseX < 300 &&
      mouseX > 150
    ) {
        if(plankY + deltaY > 455){
            deltaY = 0
            plankY +=deltaY
        }
        else if(plankY + deltaY < 15){
            deltaY = 0
            plankY +=deltaY
        }
        else{
            plankY += deltaY;
        }
    }
  }



function mousePressed() {
    // Проверка, находится ли текущее положение мыши внутри заданной зоны (например, прямоугольника кнопки)
    if (mouseX > buttonX && mouseX < buttonX + buttonWidth && mouseY > buttonY && mouseY < buttonY + buttonHeight) {
      toggleButton();
    }
}

function toggleButton() {
    // Инвертирование значения переменной on при клике
    on = !on;
    voltageValue = 0;

    targetVoltageAngle = 30;

    targetAmperAngle = 30;
}

function mouseWheel(event) {
    if(isMouseInsideCircle(mouseX, mouseY)){
        // Получаем значение вращения колесика мыши
        let value = event.deltaY;
        // Изменяем угол вращения в зависимости от направления вращения колесика
        if (voltageValue >= 1.5 && value > 0) {
            voltageValue = 1.5;
        } else if (voltageValue <= 0 && value < 0) {
            voltageValue = 0;
        } else {
            voltageValue += value / 5000;
        }
        // console.log(voltageValue)
    
        // Предотвращаем прокрутку страницы
        return false;
    }
}

function isMouseInsideCircle(mouseX, mouseY) {
    var distance = Math.sqrt(Math.pow(mouseX - circleX, 2) + Math.pow(mouseY - circleY, 2));
    return distance <= circleRadius;
}

function voltagenArrow() {

    if(on){
        // Рисуем стрелку с концом, который перемещается к заданным координатам
        targetVoltageAngle = 31 + voltageValue * 78;
        let arrowEndX = arrowBaseX - cos(radians(currentVoltageAngle)) * arrowLength;
        let arrowEndY = arrowBaseY - sin(radians(currentVoltageAngle)) * arrowLength;

        line(arrowBaseX, arrowBaseY, arrowEndX, arrowEndY);
    }
    else{
        let arrowEndX = arrowBaseX - cos(radians(currentVoltageAngle)) * arrowLength;
        let arrowEndY = arrowBaseY - sin(radians(currentVoltageAngle)) * arrowLength;
        line(arrowBaseX, arrowBaseY, arrowEndX, arrowEndY);
    }
    
}


function amperArrow() {

    let aVal = calculateAmper();

    if(on){
        // Рисуем стрелку с концом, который перемещается к заданным координатам
        targetAmperAngle = 32 + aVal * 464;
        let AmperArrowEndX = AmperArrowBaseX - cos(radians(currentAmperAngle)) * AmperArrowLength;
        let AmperArrowEndY = AmperArrowBaseY - sin(radians(currentAmperAngle)) * AmperArrowLength;
        line(AmperArrowBaseX, AmperArrowBaseY, AmperArrowEndX, AmperArrowEndY);
    }
    else{
        let AmperArrowEndX = AmperArrowBaseX - cos(radians(currentAmperAngle)) * AmperArrowLength;
        let AmperArrowEndY = AmperArrowBaseY - sin(radians(currentAmperAngle)) * AmperArrowLength;
        line(AmperArrowBaseX, AmperArrowBaseY, AmperArrowEndX, AmperArrowEndY);
    }
    
}

function calculateResistance() {
    let resistance = 0.00001194*(length/0.000001)
    // console.log(resistance);
    return resistance
}

function calculateAmper(){
    amperValue = voltageValue/calculateResistance()
    if(amperValue > 0.248){
        amperValue = 0.250
    }
    // console.log(amperValue);
    return amperValue
}


function updateArrows() {
    currentVoltageAngle = lerp(currentVoltageAngle, targetVoltageAngle, 0.05);
    currentAmperAngle = lerp(currentAmperAngle, targetAmperAngle, 0.05);
  }