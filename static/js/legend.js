var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        region_c = ["CR", "NR","ER","NER","WR"],
        labels = ["#66c2a5","#fc8d62","#8da0cb","#e78ac3","#a6d854"];
        region_n =["Central Region","North Region","East Region","North East Region","West Region"];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < region_c.length; i++) {
      div.innerHTML +=
      '<i style="background:' + labels[i] + '"></i> ' +
      region_n[i]+'-'+'<b>['+region_c[i]+ ']</b><br>';
}
    return div;
};
