var app = angular.module('plannerApp');
/*********************************/
/*      PLANNER CONTROLLER       */
/*********************************/
app.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller via the StudentService factory
  $scope.theStudent = {};
  $scope.theCourse = {};
  $scope.theTemplate = {};
  $scope.originalPlan = {};
  $scope.thePlan = {};
  $scope.semColors = [];
  $scope.tableWidth = document.getElementById('template-table').clientWidth;

  //Watcher for new selected student.
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      $scope.theStudent = newValue;
    }
  });

  //Watched for newly retrieved template + plan
  $scope.$watch(function () { return StudentService.getChangedJSON(); }, function (newValue, oldValue) {
    var theJSON = {};
    angular.copy(StudentService.getJSON(), theJSON);
    //Handle new template
    $scope.theTemplate = theJSON.template;

    //Handle new plan
    $scope.semColors = [];
    thePlan = theJSON.plan;
    angular.forEach(thePlan, function(year, yearIndex) {
      angular.forEach(year, function(sem, semIndex) {
        if(sem.length !== 0) {
          insertSemHeader(sem, yearIndex, semIndex);
        };
      });
    });
    $scope.originalPlan = thePlan;
    $scope.thePlan = thePlan;
  });

  //Determines the style of the cell based on template/plan information
  $scope.templateCellStyle = function(unit) {
    var style = {}
    //Resize based on credits
    if(unit.credits === 12.5) {
      style['width'] = '11%';
      style['font-size'] = '12px';
    }
    else if(unit.credits === 50.0) {
      style['width'] = '44%';
    }
    //Colour of fill/font based on template status/planned semester
    if(unit.status === 'PASS') {
      style['background-color'] = '#297E2B';
      style['color'] = '#FFFFFF';
    }
    else {
      var colorStyle = findUnitStyleInPlan(unit);
      style['background-color'] = colorStyle['background-color'];
      style['color'] = colorStyle['color'];
    }
    return style;
  }

  function findUnitStyleInPlan(unit) {
    colorStyle = {};
    angular.forEach($scope.thePlan, function(year, yearIndex) {
      angular.forEach(year, function(sem, semIndex) {
        angular.forEach(sem, function(planUnit) {
          if(unit.id === planUnit.id) {
            colorStyle['background-color'] = $scope.semColors[yearIndex][semIndex];
            colorStyle['color'] = '#FFFFFF';
          }
        });
      });
    });
    return colorStyle;
  }

  //Checks if row is header or unit and renders accordingly.
  $scope.renderPlannerRow = function(row) {
    rendered = ''
    if(angular.equals(row.type, 'heading')) {
      rendered = 'Year ' + row.year + ', Semester ' + row.semester;
    }
    else {
      rendered = row.name + ' - ' + row.credits + ' credits'
    }
    return rendered;
  };

  $scope.stylePlannerRow = function(unitObj, yearIndex, semIndex) {
    style = {};
    if(unitObj.type === 'heading') {
      style['background-color'] = $scope.semColors[yearIndex][semIndex];
    }
    return style;
  }

  $scope.addSemHeader = function() {
    //TODO: Verify input to make sure semester is below 3
    //      and year is below like 6 idk
    var yearToInsert = $scope.semHeaderYearInput;
    var semToInsert = $scope.semHeaderSemInput;
    var thePlan = $scope.thePlan;
    if(typeof yearToInsert === 'undefined' || typeof semToInsert === 'undefined' ||yearToInsert > 6 || semToInsert > 2) {
      //Show Error Message
    }
    else {
      thePlan = arrayInsertAndNullify(thePlan, yearToInsert-1);
      thePlan[yearToInsert - 1] = arrayInsertAndNullify(thePlan[yearToInsert - 1], semToInsert - 1);

      var theUnits = thePlan[yearToInsert - 1][semToInsert - 1];
      if(theUnits.length === 0) {
        insertSemHeader(theUnits, yearToInsert-1, semToInsert-1);
      }
    }
  }

  function insertSemHeader(array, yearIndex, semIndex) {
    array.unshift({'type': 'heading',
                 'year': (yearIndex + 1),
                 'semester': (semIndex + 1)});
    arrayInsertAndNullify($scope.semColors, yearIndex);
    arrayInsertAndNullify($scope.semColors[yearIndex], semIndex);
    $scope.semColors[yearIndex][semIndex] = genRandomColor($scope.semColors);
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
      text = 'Att: ' + attempts;
    }
    return text;
  };

  //Back button
  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }
});
