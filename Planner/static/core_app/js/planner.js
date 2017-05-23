angular.module('plannerApp')
.controller('plannerCtrl', function($scope, StudentService) {
  $scope.theStudent = '';
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) $scope.theStudent = newValue;
  });

  var theButton = document.getElementById('edit-plan');
  theButton.onclick = function () {
    console.log($scope.theStudent);
  }
});
