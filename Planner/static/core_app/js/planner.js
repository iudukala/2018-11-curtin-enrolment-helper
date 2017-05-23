angular.module('plannerApp')
.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller
  $scope.theStudent = {};
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) $scope.theStudent = newValue;


  $scope.backToStudents = function () {
    $rootScope.selectingStudent = true;
  }
  });
});
