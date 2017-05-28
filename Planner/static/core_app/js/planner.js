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
  $scope.selectedYearIndex = -1;
  $scope.selectedSemIndex = -1;
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
    $scope.theCourse = theJSON.course;
    $scope.selectedYearIndex = -1;
    $scope.selectedSemIndex = -1;

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
      var colorStyle = findTemplateUnitColor(unit);
      style['background-color'] = colorStyle['background-color'];
      style['color'] = colorStyle['color'];
    }
    return style;
  }

  function findTemplateUnitColor(unit) {
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
    var yearToInsert = $scope.semHeaderYearInput;
    var semToInsert = $scope.semHeaderSemInput;
    var thePlan = $scope.thePlan;
    if(!validSemesterHeaderInput(yearToInsert, semToInsert) ) {
      showErrorMessage("Error: Invalid semester header input.")
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

  function validSemesterHeaderInput(year, sem) {
    return (typeof year !== 'undefined' && typeof sem !== 'undefined' &&
             year > 0 && year < 7 && sem > 0 && sem < 3);
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

  $scope.plannerTrashClick = function(unit, yearIndex, semIndex) {
    //If heading, remove all units.
    if(unit.type === 'heading') {
      removePlanSem(yearIndex, semIndex);
    }
    //If unit, remove only that unit.
    else {
      removePlanUnit(unit.id);
    }
  }

  $scope.addUnitToPlan = function(unit) {
    selectedYear = $scope.selectedYearIndex;
    selectedSem = $scope.selectedSemIndex
    if(unit.status === 'PASS') {
      showErrorMessage("Error: Unit selected already passed.")
    }
    else if(selectedYear < 0 || selectedSem < 0) {
      showErrorMessage("Error: Please select a semester to assign this unit to.")
    }
    else {
      removePlanUnit(unit.id);
      $scope.thePlan[selectedYear][selectedSem].push(unit);
    }
  }

  function removePlanSem(yearIndex, semIndex) {
    $scope.thePlan[yearIndex][semIndex] = [];
    $scope.semColors[yearIndex][semIndex] = '';
    $scope.selectedYearIndex = -1;
    $scope.selectedSemIndex = -1;
  }

  function removePlanUnit(unitID) {
    angular.forEach($scope.thePlan, function(year, yearIndex) {
        angular.forEach(year, function(sem, semIndex) {
          angular.forEach(sem, function(planunit, unitIndex) {
            if(unitID === planunit.id) {
              $scope.thePlan[yearIndex][semIndex].splice(unitIndex, 1);
            }
          });
        });
    });
  }

  $scope.plannerBucketClick = function(yearIndex, semIndex) {
    $scope.selectedYearIndex = yearIndex;
    $scope.selectedSemIndex = semIndex;
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

  //Error message
  function showErrorMessage(inputMessage) {
    $scope.errorText = inputMessage
    $scope.errorMessage = true;
    setTimeout(function() {
      $scope.errorMessage = false;
      $scope.$apply();
    }, 4000);
  }
});
