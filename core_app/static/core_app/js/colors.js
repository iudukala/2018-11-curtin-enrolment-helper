var colors = ['#E86830', '#C71F16', '#C7166F', '#8930E8', '#F49CC8', '#3080E8',
              '#30C9E8', '#30E8BD', '#E8E230', '#E8B730', '#C67D53', '#A5E830']

function genRandomColor(colorArray) {
  color = '';
  do {
      color = colors[Math.floor(Math.random() * colors.length)];
  }
  while(array2DContains(colorArray, color) && colorArray.length < colors.length);
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
