angular.module('plannerApp')
.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller via the StudentService factory
  $scope.theStudent = {};
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) $scope.theStudent = newValue;
  });

  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }

  var receivedJSON = {
    template: {
                1 : {
                      1 : {
                        COMP2003 : { name: 'OOSE', credits: 25.0 },
                        COMP1001: { name: 'OOPD', credits: 25.0 }
                      },
                			2: {
                        COMP1000 : { name: 'UCP', credits: 12.5 },
                        COMP1002: { name: 'DSA', credits: 25.0 }
                      }
                    },
                2 : {
                    	1 : {
                        COMP3001 : { name: 'DAA', credits: 25.0 },
                        ISAD1000: { name: 'ISE', credits: 25.0 }
                      },
                			2: {
                        COMP2003 : { name: 'OOSE', credits: 25.0 },
                        COMP1001: { name: 'OOPD', credits: 25.0 }
                      }
                    }
              },
    plan: {}
  }

  angular.forEach(receivedJSON.template, function (semObj, yearNum) {
    angular.forEach(semObj, function(unitListObj, semNum) {
      angular.forEach(unitListObj, function(unitObj, unitID) {
        //Make data structure
      });
    });
  });
});
