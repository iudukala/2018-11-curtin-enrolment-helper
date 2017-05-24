/*********************************/
/*      ANGULAR APP SETUP        */
/*********************************/
var app = angular.module('plannerApp', [])
.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});
//Factory for sharing student name with planner controller
app.factory('StudentService', function() {
  var selectedStudent = {};

  return {
      getStudent: function () {
          return selectedStudent;
      },
      setStudent: function (studentObj) {
         selectedStudent = studentObj;
      }
  };
});
/*********************************/
/*    ANGULAR APP CONTROLLER     */
/*********************************/
app.controller('studentSelectCtrl', function($scope, $rootScope, StudentService) {
  $scope.students = [];
  $scope.selectedStudent = {};
  $scope.$watch('selectedStudent', function (newValue, oldValue) {
      if (newValue !== oldValue) StudentService.setStudent(newValue);
  });

  $scope.selectStudent = function(id, name) {
    $scope.selectedStudent = {name: name, id: id};
  };

  $scope.studentIsEmpty = function() {
    return angular.equals($scope.selectedStudent, {})
  };

  $scope.gotoPlanner = function() {
    if(!$scope.studentIsEmpty()) {
      $rootScope.selectingStudent = false;
    }
  };

  //INITIALIZATION OF DATA
  var json =  { '16171921': 'Campbell Pedersen',
                '16365481': 'Chung-Yen Lu',
                '16102183': 'Chen Bi',
                '17080170': 'Yoakim Persson',
                '17898755': 'Thien Quang Trinh'
              };

  //Append student JSON to array
  angular.forEach(json, function (value, key) {
    $scope.students.push({'id': key, 'name': value});
  });
});
//Controls display of each page
app.run(function($rootScope) {
  $rootScope.selectingStudent = true;
});
