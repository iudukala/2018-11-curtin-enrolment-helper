var app = angular.module('plannerApp');
/*********************************/
/*      PLANNER CONTROLLER       */
/*********************************/
app.controller('plannerCtrl', function($scope, $http, $rootScope, StudentService) {
  $scope.theStudent = {};
  $scope.theCourse = {};
  $scope.theTemplate = {};
  $scope.originalPlan = {};
  $scope.thePlan = {};
  $scope.selectedYearIndex = -1;
  $scope.selectedSemIndex = -1;
  $scope.semColors = [];

  /*
   * Name: $watch getStudent
   *
   * Purpose: Fires when the user selects a new student, on the
   *          student select page, and updates the scope to reflect this.
   *
   * Params: newValue and Oldvalue, pretty self explanitory.
   *
   * Return: none.
   *
   * Notes: N/A.
   */
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) {
      $scope.theStudent = newValue;
    }
  });


  /*
   * Name: $watch getChangedJSON
   *
   * Purpose: Watches for when a new student is selected and
   *          a new JSON is requested.
   *
   * Params: newValue and oldValue, the new and old template + plan objects.
   *
   * Return: none.
   *
   * Notes: N/A.
   */
  $scope.$watch(function () { return StudentService.getChangedJSON(); }, function (newValue, oldValue) {
    var theJSON = {};
    theJSON = angular.copy(StudentService.getJSON());
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
    $scope.originalPlan = angular.copy(thePlan);
    $scope.thePlan = angular.copy(thePlan);
  });


  /*
   * Name: styleTemplateCell
   *
   * Purpose: Determines the stylings of each template cell in
   *          the template table.
   *
   * Params: unit, the unit object associated with that template cell.
   *
   * Return: A JSON object, in line with the HTML styling specification.
   *
   * Notes: N/A
   */
  $scope.styleTemplateCell = function(unit) {
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


  /*
  * Name: findTemplateUnitColor
  *
  * Purpose: Finds the specific colour that a template cell should be.
  *          This is determined by unit status and the student plan displayed.
  *
  * Params: unit, the unit object of the template cell being styled.
  *
  * Return: a JSON in line with the HTML styling specification.
  *
  * Notes: Called by templateCellStyle.
  */
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

/*
 * Name: renderPlannerRow
 *
 * Purpose: Determines the text that is displayed in a particular
 *          planner table row.
 *
 * Params: row, the row object associated with that row.
 *
 * Return: A string, the text to be displayed in the planner cell.
 *
 * Notes: N/A
 */
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

  /*
   * Name: stylePlannerRow
   *
   * Purpose: Determines the styling of a planner row, based on the row object
   *
   * Params: rowObj, the row object
   *         yearIndex, the year the row is in
   *         semeIndex, the semester the row is in
   *
   * Return: A JSON object, in line with the HTML styling specification.
   *
   * Notes: Called by renderPlannerRow
   */
  $scope.stylePlannerRow = function(rowObj, yearIndex, semIndex) {
    var style = {};
    if(rowObj.type === 'heading') {
      style['background-color'] = $scope.semColors[yearIndex][semIndex];
    }
    return style;
  }

  /*
   * Name: styleSemColor
   *
   * Purpose: Determines the styling of the selected sem square
   *
   * Params: none.
   *
   * Return: A JSON object, in line with the HTML styling specification.
   *
   * Notes: Set as the ng-style of selected-semester-color
   */
  $scope.styleSemColor = function() {
    var style = {}
    var selectedYear = $scope.selectedYearIndex;
    var selectedSem = $scope.selectedSemIndex;
    if(selectedYear > -1 && selectedSem > -1) {
      style = {'background-color': $scope.semColors[selectedYear][selectedSem]};
    }
    return style;
  }

  /*
   * Name: addSemHeader
   *
   * Purpose: Adds a semester header to the planner table
   *
   * Params: N/A
   *
   * Return: none.
   *
   * Notes: add-sem-header-button has this method as its ng-click attribute
   */
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
      else {
        showErrorMessage("Semester already exists.")
      }
    }
  }

  /*
   * Name: validSemesterHeaderInput
   *
   * Purpose: Checks if a year and semester input by the user is valid or not
   *
   * Params: year, the year input
   *         sem, the semester input
   *
   * Return: boolean, true if input is valid.
   *
   * Notes: called by addSemHeader
   */
  function validSemesterHeaderInput(year, sem) {
    return (typeof year !== 'undefined' && typeof sem !== 'undefined' &&
             year > 0 && year < 7 && sem > 0 && sem < 3);
  }

  /*
   * Name: insertSemHeader
   *
   * Purpose: Inserts a semester header into the plan
   *
   * Params: array, the plan array
   *         yearIndex, the year index to insert the header
   *         semIndex, the semester index to insert the header
   *
   * Return: boolean, true if input is valid.
   *
   * Notes: N/A
   */
  function insertSemHeader(array, yearIndex, semIndex) {
    array.unshift({'type': 'heading',
                   'id': 'HEADING',
                   'year': (yearIndex + 1),
                   'semester': (semIndex + 1)});
    arrayInsertAndNullify($scope.semColors, yearIndex);
    arrayInsertAndNullify($scope.semColors[yearIndex], semIndex);
    $scope.semColors[yearIndex][semIndex] = genRandomColor($scope.semColors);
  }

  /*
   * Name: arrayInsertAndNullify
   *
   * Purpose: Takes an array, and inserts empty array indexes
   *          into it until the specified index is readched
   *
   * Params: array, the array to be filled
   *         index, the index to fill until
   *
   * Return: boolean, true if input is valid.
   *
   * Notes: N/A
   */
  function arrayInsertAndNullify(array, index) {
    for(var i = 0; i < index + 1; i++) {
      if(typeof array[i] === 'undefined') {
        array[i] = [];
      }
    }
    return array;
  }

  /*
   * Name: plannerTrashClick
   *
   * Purpose: Deletes a unit/semester from the enrolment plan
   *
   * Params: row, the row object representing the planner row to delete
   *         yearIndex, the year the specified row is in
   *         semIndex, the semester the specified row is in
   *
   * Return: boolean, true if input is valid.
   *
   * Notes: Set as the ng-click directive of each trash icon in the planner list
   */
  $scope.plannerTrashClick = function(row, yearIndex, semIndex) {
    //If heading, remove all units from that semester, and the header.
    if(row.type === 'heading') {
      removePlanSem(yearIndex, semIndex);
    }
    //If unit, remove only that unit.
    else {
      removePlanUnit(row.id);
    }
  }

  /*
   * Name: removePlanSem
   *
   * Purpose: Removes an entire semester from the plan
   *
   * Params: yearIndex and semIndex, the indexes of the semester to remove
   *
   * Return: none.
   *
   * Notes: Called by plannerTrashClick
   */
  function removePlanSem(yearIndex, semIndex) {
    $scope.thePlan[yearIndex][semIndex] = [];
    $scope.semColors[yearIndex][semIndex] = '';
    if(yearIndex === $scope.selectedYearIndex && semIndex === $scope.selectedSemIndex) {
      $scope.selectedYearIndex = -1;
      $scope.selectedSemIndex = -1;
    }
  }

  /*
   * Name: removePlanUnit
   *
   * Purpose: Removes all instances of a single unit from the plan
   *
   * Params: unitID, the unit ID of the unit to remove
   *
   * Return: none.
   *
   * Notes: Called by plannerTrashClick
   */
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

  /*
   * Name: addUnitToPlan
   *
   * Purpose: Adds a unit to to the plan
   *
   * Params: unit, the unit object to add to the plan
   *
   * Return: none.
   *
   * Notes: Set as the ng-click directive of each cell in the template
   */
  $scope.addUnitToPlan = function(unit) {
    selectedYear = $scope.selectedYearIndex;
    selectedSem = $scope.selectedSemIndex
    if(unit.status === 'PASS') {
      showErrorMessage("Unit selected has already been passed.")
    }
    else if(selectedYear < 0 || selectedSem < 0) {
      showErrorMessage("Please select a semester to assign this unit to.")
    }
    else {
      removePlanUnit(unit.id);
      $scope.thePlan[selectedYear][selectedSem].push(unit);
    }
  }

  /*
   * Name: plannerBucketClick
   *
   * Purpose: Selects a new year/semester to paintbucket
   *
   * Params: yearIndex, semIndex, the year/semester selected
   *
   * Return: none.
   *
   * Notes: Set as the ng-click directive of the paintbucket icon
   */
  $scope.plannerBucketClick = function(yearIndex, semIndex) {
    $scope.selectedYearIndex = yearIndex;
    $scope.selectedSemIndex = semIndex;
  }

  /*
   * Name: getUnitAttemptsText
   *
   * Purpose: Determines the text to be shown in each template cell's attempts span
   *
   * Params: attempts, the number of attempts a unit has had
   *         status: the status of said unit
   *
   * Return: a string, the text to be shown
   *
   * Notes: Binded to each template cell's attempts span
   */
  $scope.getUnitAttemptsText = function(attempts, status) {
    text = '';
    if(status !== 'PASS' && attempts !== 0) {
      text = 'Att: ' + attempts;
    }
    return text;
  };

  /*
   * Name: backToStudents
   *
   * Purpose: Takes the user back to the student select page
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: N/A
   */
  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }

  /*
   * Name: resetPlan
   *
   * Purpose: Resets the displayed plan to the original plan saved in the database.
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: Set as the ng-click attribute of the reset plan button
   */
  $scope.resetPlan = function() {
    //Reset plan object
    $scope.thePlan = angular.copy($scope.originalPlan);
    //Assign new colours to each header
    angular.forEach($scope.thePlan, function(year, yearIndex) {
        angular.forEach(year, function(sem, semIndex) {
          angular.forEach(sem, function(planunit, unitIndex) {
            if(planunit.type === 'heading' && !$scope.semColors[yearIndex][semIndex]) {
              $scope.semColors[yearIndex][semIndex] = genRandomColor($scope.semColors);
            }
          });
        });
    });
    $scope.selectedYearIndex = -1;
    $scope.selectedSemIndex = -1;
  }

  /*
   * Name: emailPlan
   *
   * Purpose: emails the stored plan in the database to
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: Set as the ng-click attribute of the email plan button
   */
  $scope.emailPlan = function() {
    studentObj = {id: $scope.theStudent.id};
    $rootScope.openSpinner('Emailing plan to student...');
    $http.post('/emailplan', studentObj).then(emailSuccess, plannerErrorHandler);
  }

  /*
   * Name: emailSuccess
   *
   * Purpose: called when the stored enrolment plan is emailed to a user successfully
   *
   * Params: response, the retrieved HTTP response from the server
   *
   * Return: none
   *
   * Notes: N/A
   */
  function emailSuccess(response) {
    showSuccessMessage("Email sent successfully.");
    $rootScope.closeSpinner();
  }

  /*
   * Name: savePlan
   *
   * Purpose: attempts to save the current enrolment plan into the database
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: Set as the ng-click attribute of the save plan button
   */
  $scope.savePlan = function() {
    $rootScope.openSpinner('Saving plan data...');
    var savedPlan = angular.copy($scope.thePlan);
    cleanupPlan(savedPlan);

    $http.post('/savePlan', savedPlan)
    .then(saveSuccess, plannerErrorHandler);
  }

  /*
   * Name: cleanupPlan
   *
   * Purpose: cleans the plan to send to the database by clearing all
   *          semester headings out of each semester, and deletes
   *          redundant years
   *
   * Params: dirtyPlan, a reference to the plan to be cleaned
   *
   * Return: none
   *
   * Notes: Called by savePlan
   */
  function cleanupPlan(dirtyPlan) {
    //Remove semester headings
    angular.forEach(dirtyPlan, function(year, yearIndex) {
        angular.forEach(year, function(sem, semIndex) {
          if(sem.length > 0 && sem[0].type === 'heading') {
            sem.shift();
          }
        });
    });

    //Remove redundant years
    var i = dirtyPlan.length - 1;
    while(isEmptyYear(dirtyPlan[i])) {
      dirtyPlan.splice(i, 1);
      i--;
    }
  }

  /*
   * Name: isEmptyYear
   *
   * Purpose: checks a specific plan year's array to see if its empty
   *
   * Params: year, a single year's array
   *
   * Return: boolean, true if the year is empty
   *
   * Notes: Called by savePlan
   */
  function isEmptyYear(year) {
    var empty = true;
    angular.forEach(year, function(sem) {
      if(sem.length !== 0) {
        empty = false;
      }
    });
    return empty;
  }

  /*
   * Name: saveSuccess
   *
   * Purpose: called when the stored enrolment plan is saved to the database successfully.
   *
   * Params: response, the retrieved HTTP response from the server
   *
   * Return: none
   *
   * Notes: N/A
   */
  function saveSuccess(response) {
    showSuccessMessage("Plan saved successfully.");
    $rootScope.closeSpinner();
  }

  /*
   * Name: plannerErrorHandler
   *
   * Purpose: called when a HTTP error response is received from the server.
   *
   * Params: response, the retrieved HTTP response from the server
   *
   * Return: none
   *
   * Notes: N/A
   */
  function plannerErrorHandler(response) {
    var endtext = response.data;
    if(!response.data) {
      endtext = response.statusText;
    }
      showErrorMessage('HTTP ERROR '+ response.status + ': ' + endtext);
      $rootScope.closeSpinner();
  };

  /*
   * Name: showSuccessMessage
   *
   * Purpose: Shows an success message on the planner's screen
   *
   * Params: inputMessage, the string to display
   *
   * Return: none
   *
   * Notes: N/A
   */
  function showSuccessMessage(inputMessage) {
    $scope.successText = inputMessage
    $scope.successMessage = true;
    setTimeout(function() {
      $scope.successMessage = false;
      $scope.$apply();
    }, 3000);
  }

  /*
   * Name: showErrorMessage
   *
   * Purpose: Shows an error message on the planner's screen
   *
   * Params: inputMessage, the string to display
   *
   * Return: none
   *
   * Notes: N/A
   */
  function showErrorMessage(inputMessage) {
    $scope.errorText = inputMessage
    $scope.errorMessage = true;
    setTimeout(function() {
      $scope.errorMessage = false;
      $scope.$apply();
    }, 3000);
  }
});
