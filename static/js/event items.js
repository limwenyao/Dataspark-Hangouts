//percentage of sentiment , id is string
// <canvas id="myCanvas" width="300" height="150" style="border:1px solid #d3d3d3;">
// Your browser does not support the HTML5 canvas tag.</canvas>
function rectangle(p,i){
  var c = document.getElementById(i);
  var ctx = c.getContext("2d");

  ctx.beginPath();
  ctx.rect(20, 20, 100, 150);
  if (p>=80){
    ctx.fillStyle = "green";
  }
  else if (50<=p<80){
    ctx.fillStyle = "yellow";
  }
  else{
    ctx.fillStyle = "red";
  }
  ctx.fill();
}
