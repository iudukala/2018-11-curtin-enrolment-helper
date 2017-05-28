var colors = ['#DC143C', '#FF7700', '#FFCC00', '#9933FF', '#0066CC',
              '#FF00FF', '#4B0082', '#A0522D', '#FFC0CB', '#C9CBFF',
              '#98FB98', '#000080']

function genRandomColor(colorArray) {
  do {
      color = colors[Math.floor(Math.random() * colors.length)];
  }
  while(array2DContains(colorArray, color));
  return color;
}

function array2DContains(array, value) {
  contains = false;
  angular.forEach(array, function(row) {
    if(row.indexOf(value) !== -1) {
      contains = true;
    }
  });
  return contains;
}
