var app = angular.module('plannerApp');
/*********************************/
/*      PLANNER CONTROLLER       */
/*********************************/
app.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller via the StudentService factory
  $scope.theStudent = {};
  $scope.theTemplate = {};
  $scope.originalPlan = {};
  $scope.thePlan = {};
  $scope.tableWidth = document.getElementById('template-table').clientWidth;

  //Watcher for new selected student.
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      $scope.theStudent = newValue;
    }
  });

  //Watched for newly retrieved template + plan
  $scope.$watch(function () { return StudentService.getJSON(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      //Handle new template
      $scope.theTemplate = newValue.template;

      //Handle new plan
      thePlan = newValue.plan;
      angular.forEach(thePlan, function(year, yearIndex) {
        angular.forEach(year, function(sem, semIndex) {
          if(sem.length !== 0) {
            sem.unshift({'type': 'heading',
                         'year': (yearIndex + 1),
                         'semester': (semIndex + 1)});
          };
        });
      });
      $scope.originalPlan = thePlan;
      $scope.thePlan = thePlan;
    }
  });

  //Determines the style of the cell based on template/plan information
  $scope.templateCellStyle = function(status, credits) {
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

  $scope.renderPlannerRow = function(row) {
    rendered = ''
    if(angular.equals(row.type, 'heading')) {
      rendered = 'Year ' + row.year + ', Semester ' + row.semester;
    }
    else {
      rendered = row.id
    }
    return rendered;
  };

  $scope.addSemHeader = function() {
    //TODO: Verify input to make sure semester is below 3
    //      and year is below like 6 idk
    var yearToInsert = $scope.semHeaderYearInput;
    var semToInsert = $scope.semHeaderSemInput;
    var thePlan = $scope.thePlan;

    thePlan = arrayInsertAndNullify(thePlan, yearToInsert-1);
    thePlan[yearToInsert - 1] = arrayInsertAndNullify(thePlan[yearToInsert - 1], semToInsert - 1);

    var theUnits = thePlan[yearToInsert - 1][semToInsert - 1];
    if(theUnits.length === 0) {
      theUnits.unshift({'type': 'heading',
                        'year': ($scope.semHeaderYearInput),
                        'semester': ($scope.semHeaderSemInput)});
    }
  }

  function arrayInsertAndNullify(array, index) {
    for(var i = 0; i < index + 1; i++) {
      if(typeof array[i] === 'undefined') {
        array[i] = [];
      }
    }
    return array;
  }

  $scope.getUnitAttemptsText = function(attempts, status) {
    text = '';
    if(status !== 'PASS' && attempts !== 0) {
      text = 'Attempts: ' + attempts;
    }
    return text;
  };

  //Back button
  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }
});
