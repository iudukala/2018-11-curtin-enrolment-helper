/*********************************/
/*       ANGULAR APP CODE        */
/*********************************/
var app = angular.module('studentSelectApp', []).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});
app.controller('studentSelectCtrl', function($scope) {
});
app.run(function($rootScope) {
  $rootScope.students = [];
  $rootScope.selectedStudentID = '';

  $rootScope.selectStudent = function(id) {
    $rootScope.selectedStudentID = id;
  };
  
  //Testing input only
  var json =  { '16171921': 'Campbell Pedersen',
                '16365481': 'Chung-Yen Lu',
                '16102183': 'Chen Bi',
                '17080170': 'Yoakim Persson',
                '17898755': 'Thien Quang Trinh' };

  //Append student JSON to array
  angular.forEach(json, function (value, key) {
    $rootScope.students.push({'id': key, 'name': value});
  });
});
