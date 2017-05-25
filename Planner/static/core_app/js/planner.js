var app = angular.module('plannerApp');
/*********************************/
/*      PLANNER CONTROLLER       */
/*********************************/
app.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller via the StudentService factory
  $scope.theStudent = {};
  $scope.theJSON = {};
  $scope.tableWidth = document.getElementById('template-table').clientWidth;

  //Watcher for new selected student.
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      $scope.theStudent = newValue;
    }
  });

  $scope.$watch(function () { return StudentService.getJSON(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      $scope.theJSON = newValue;
    }
  });


  //Back button
  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }

  //Determines the style of the cell based on template/plan information
  $scope.cellStyle = function(status, credits) {
    var style = {}
    //Resize based on credits
    if(credits === 12.5) {
      style['width'] = '11%';
      style['font-size'] = '12px';
    }
    else if(credits === 50.0) {
      style['width'] = '44%';
    }
    //Colour of fill/font based on template status/planned semester
    if(status === 'PASS') {
      style['background-color'] = '#297E2B';
      style['color'] = '#FFFFFF';
    }
    return style;
  }

  $scope.getUnitAttemptsText = function(attempts, status) {
    text = '';
    if(status !== 'PASS' && attempts !== 0) {
      text = 'Attempts: ' + attempts;
    }
    return text;
  }

});
