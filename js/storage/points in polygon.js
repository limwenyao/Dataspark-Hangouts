//function that checks whether the markers are inside a subzone
var testCoordinates2 =  [[1.3521, 103.8198],[1.2798070057318836,103.83961460585509]];
function getTurfPoints(coordinates){
  var temp = [];
  for (i =0;i<coordinates.length;i++){
    temp.push([coordinates[i][0],coordinates[i][1]]); //add the points

  }
  console.log(temp[0]);
  return temp;
}
var point = turf.points([[103.83961460585509,1.2798070057318836],[1.3521, 103.8198]]);
// here first is lng and then lat
var polygon = turf.polygon([[
 [103.83961460585509,1.2798070057318836],[103.83810885041181,1.2817688912647172],[103.84071799267522,1.2823945500071308],[103.84282640070447,1.2846312969825842],[103.84335493257873,1.2841954462359355],[103.83961460585509,1.2798070057318836]
]], { name: 'poly1'});
// here first is lng and then lat
var ptsWithin = turf.pointsWithinPolygon(point, polygon);
if (ptsWithin.length==1){
 alert("one!");
}
else{
 alert("No");
}
//alert(turf.inside(point, polygon));
