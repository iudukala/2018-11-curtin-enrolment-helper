/*********************************/
/*       ANGULAR APP CODE        */
/*********************************/
var app = angular.module('plannerApp', [])
.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});
//Factory for sharing student name with planner controller
app.factory('StudentService', function() {
  var selectedStudent = ''

  return {
      getStudent: function () {
          return selectedStudent
      },
      setStudent: function (id) {
         selectedStudent = id;
      }
  };
});

app.controller('studentSelectCtrl', function($scope, StudentService) {
  $scope.students = [];
  $scope.selectedStudentID = '';
  $scope.$watch('selectedStudentID', function (newValue, oldValue) {
      if (newValue !== oldValue) StudentService.setStudent(newValue);
  });

  $scope.selectStudent = function(id) {
    $scope.selectedStudentID = id;
  }

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
