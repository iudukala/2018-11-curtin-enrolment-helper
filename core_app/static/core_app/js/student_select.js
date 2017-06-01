/*********************************/
/*      ANGULAR APP SETUP        */
/*********************************/
var app = angular.module('plannerApp', [])
.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});
/*
 * Name: StudentService factory
 *
 * Purpose: A service to pass the selected student object between the student
 *          selection controller and the planner controller
 *
 * Params: none
 *
 * Return: An object with various functions to get the selected student object
 *
 * Notes: N/A
 */
app.factory('StudentService', function() {
  var selectedStudent = {};
  var theJSON = {};
  var changedJSON = true;

  return {
      getStudent: function () {
        return selectedStudent;
      },
      setStudent: function (studentObj) {
        selectedStudent = studentObj;
      },
      getJSON: function () {
        return theJSON;
      },
      setJSON: function (jsonOBJ) {
        theJSON = jsonOBJ;
        changedJSON = !changedJSON;
      },
      getChangedJSON: function() {
        return changedJSON;
      }
  };
});
/*********************************/
/* STUDENT SELECTION CONTROLLER  */
/*********************************/
app.controller('studentSelectCtrl', function($scope, $rootScope, $http, StudentService) {
  //INITIALIZATION OF DATA
  $scope.errorText = '';
  $scope.errorMessage = false;
  $scope.students = [];
  $scope.selectedStudent = {};
  $scope.gettingStudentTemplate = false;

  /*
   * Name: $watch.selectedStudent
   *
   * Purpose: Fires when the user selects a new student, and updates
   *          the service to reflect the new changes
   *
   * Params: newValue and oldValue, pretty self-explanitory.
   *
   * Return: none
   *
   * Notes: N/A
   */
  $scope.$watch('selectedStudent', function (newValue, oldValue) {
    StudentService.setStudent(newValue);
  });

  /*
   * Name: showErrorMessage
   *
   * Purpose: Shows a brief error message on screen
   *
   * Params: inputMessage, the string to be shown
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
    }, 4000);
  }

  /*
   * Name: getStudentList
   *
   * Purpose: Sets up an AJAX request to retrieve the list of students
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: N/A
   */
  function getStudentList() {
    $rootScope.openSpinner('Loading student list...');
    //Uncomment when merging
    $http.get('/getStudentList').then(studentListHandler, studentSelectErrorHandler);

    // setTimeout(studentListHandler, 1000);
  };

  /*
   * Name: studentListHandler
   *
   * Purpose: Callback function for successful student list AJAX request
   *
   * Params: response, the http response
   *
   * Return: none
   *
   * Notes: N/A
   */
  function studentListHandler(response) {
    //var json = response.data;
    var json = response.data;

    /*TEST DATA*/
    $scope.students = json;
    $rootScope.closeSpinner();
    $rootScope.$apply();
  }

  /*
   * Name: studentListHttpErrorHandler
   *
   * Purpose: Callback function for failed AJAX request on student select page
   *
   * Params: response, the http error response
   *
   * Return: none
   *
   * Notes: N/A
   */
  function studentSelectErrorHandler(response) {
      showErrorMessage('HTTP ERROR '+ response.status + ': ' + response.statusText);
      $rootScope.closeSpinner();
  };

  /*
   * Name: gotoPlanner
   *
   * Purpose: Sets up an AJAX request to get a students course template and
   *          enrolment plan from the back-end.
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: N/A
   */
  $scope.gotoPlanner = function() {
    if(!$scope.studentIsEmpty()) {
      $rootScope.openSpinner('Fetching student data...');
      var studentInput = { id: $scope.selectedStudent.id };
      //$http.post('/getStudentTemplate', studentInput)
      //.then(templateHandler, studentSelectErrorHandler);
      templateHandler(parsedJSON);
    }
  };

  /*
   * Name: selectStudent
   *
   * Purpose: Updates the scope to a newly selected student
   *
   * Params: id and name of the selected student
   *
   * Return: none
   *
   * Notes: N/A
   */
  function templateHandler(response) {
    //StudentService.setJSON(response.data);
    //$rootScope.closeSpinner();
    //$rootScope.selectingStudent = false;

    StudentService.setJSON(response);
    setTimeout(function() {
      $rootScope.closeSpinner();
      $rootScope.selectingStudent = false;
      $rootScope.$apply();
    }, 3000);
  }

  /*
   * Name: selectStudent
   *
   * Purpose: Updates the scope to a newly selected student
   *
   * Params: id and name of the selected student
   *
   * Return: none
   *
   * Notes: N/A
   */
  $scope.selectStudent = function(id, name) {
    $scope.selectedStudent = {name: name, id: id};
  };

  /*
   * Name: studentIsEmpty
   *
   * Purpose: Checks if the current selected student is empty
   *
   * Params: none
   *
   * Return: true if student is empty, false if student has content
   *
   * Notes: N/A
   */
  $scope.studentIsEmpty = function() {
    return angular.equals($scope.selectedStudent, {})
  };

  //Invoke this method when the controller is fully loaded
  getStudentList();
});

//Method runs when angular app runs
app.run(function($rootScope) {
  //rootScope setup
  $rootScope.selectingStudent = true;
  $rootScope.$on('$viewContentLoaded', function(){
    $rootScope.loaded = true;
  });

  //Spinner functions open and close the spinner
  $rootScope.openSpinner = function(message) {
    $rootScope.loading = true;
    $rootScope.loadingMessage = message;
  };
  $rootScope.closeSpinner = function() {
    $rootScope.loading = false;
  }
});




















/***********************************************************************************************************/
var testStudents = [{ 'id': '16171921', 'name': 'Campbell Pedersen'},
                    { 'id': '16365481', 'name': 'Chung-Yen Lu'},
                    { 'id': '16102183', 'name': 'Chen Bi'},
                    { 'id': '17080170', 'name': 'Yoakim Persson'},
                    { 'id': '17898755', 'name': 'Thien Quang Trinh'},
                    { 'id': '17160182', 'name': 'Scott Ryan Day'},
                    { 'id': '17420420', 'name': 'Ash Tulett'},
                    { 'id': '16685281', 'name': 'Tim Cochrane'},
                    { 'id': '16402918', 'name': 'Jordan Van-Elden'},
                    { 'id': '17281204', 'name': 'Aidan Noël Jolly'},
                    { 'id': '17295891', 'name': 'Sam Barker'}];

var parsedJSON = {
  course: { name: 'Software Engineering (BEng)', id: '313605' },
  template: [//Array of years
              [//Year 1
                [//Sem 1 Unit Objects
                  {id: 'MATH2012', name: 'E. Maths 120', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'MCEN1000', name: 'E. Mech 100', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'INDE1000', name: 'EF: P&C 100', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1004', name: 'E. Prog 100', credits: 12.5, status: 'PASS', attempts: 1},
                  {id: 'ELECTIVE1', name: 'ELECTIVE', credits: 12.5, status: 'PASS', attempts: 1},
                ],
                [//Sem 2 Unit Objects
                  {id: 'MATH1003', name: 'E. Maths 140', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'INDE1001', name: 'EF: D&P 100', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'ELEN1000', name: 'E. Sys 100', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'MAEN1000', name: 'E. Mat 100', credits: 25.0, status: 'PASS', attempts: 1},
                ]
              ],
              [//Year 2
                [//Sem 1 Unit Objects
                  {id: 'ISAD1000', name: 'SE 110', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1001', name: 'OOPD 100', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'STAT1002', name: 'SDA 101', credits: 12.5, status: 'PASS', attempts: 1},
                  {id: 'PRJM2000', name: 'PSP', credits: 12.5, status: 'PASS', attempts: 1},
                  {id: 'ELECTIVE2', name: 'ELECTIVE', credits: 25.0, status: 'PASS', attempts: 1}
                ],
                [//Sem 2 Unit Objects
                  {id: 'COMP1002', name: 'DSA', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1000', name: 'UCP 120', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'ISYS1001', name: 'DS 120', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'CMPE2002', name: 'RE', credits: 25.0, status: 'PASS', attempts: 1}
                ]
              ],
              [//Year 3
                [//Sem 1 Unit Objects
                  {id: 'COMP3001', name: 'DAA', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'ELECTIVE3', name: 'ELECTIVE', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'ISAD4002', name: 'SM 400', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'CNCO2000', name: 'CC', credits: 25.0, status: 'PLN', attempts: 0}
                ],
                [//Sem 2 Unit Objects
                  {id: 'CMPE3008', name: 'SET', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'ICTE3002', name: 'HCI 400', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP2004', name: 'CG 200', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP2003', name: 'OO SE', credits: 25.0, status: 'PLN', attempts: 0}
                ]
              ],
              [//Year 4
                [//Sem 1 Unit Objects
                  {id: 'BLAW2000', name: 'Eng. Law', credits: 12.5, status: 'PLN', attempts: 0},
                  {id: 'ELECTIVE4', name: 'ELECTIVE', credits: 12.5, status: 'PLN', attempts: 0},
                  {id: 'ENEN2000', name: 'ESD 201', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'ISAD4000', name: 'SEP A', credits: 50.0, status: 'PLN', attempts: 0},
                ],
                [//Sem 2 Unit Objects
                  {id: 'MGMT3000', name: 'E Man', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP3003', name: 'SE Concepts', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'ISAD4001', name: 'SEP B', credits: 50.0, status: 'PLN', attempts: 0}
                ]
              ],
            ],
  plan: [//Array of years
          [//Year 1
            [//Sem 1 Unit Objects
              {id: 'COMP3001', name: 'DAA', credits: 25.0},
              {id: 'ELECTIVE3', name: 'ELECTIVE1', credits: 25.0},
              {id: 'ISAD4002', name: 'SM 400', credits: 25.0},
              {id: 'CNCO2000', name: 'CC', credits: 25.0}
            ],
            [//Sem 2 Unit Objects
              {id: 'CMPE3008', name: 'SET', credits: 25.0},
              {id: 'ICTE3002', name: 'HCI 400', credits: 25.0},
              {id: 'COMP2004', name: 'CG 200', credits: 25.0},
              {id: 'COMP2003', name: 'OO SE', credits: 25.0}
            ]
          ],
          [//Year 2
            [//Sem 1 Unit Objects
              {id: 'BLAW2000', name: 'Eng. Law', credits: 12.5},
              {id: 'ELECTIVE4', name: 'ELECTIVE2', credits: 12.5},
              {id: 'ENEN2000', name: 'ESD 201', credits: 25.0},
              {id: 'ISAD4000', name: 'SEP A', credits: 50.0}
            ],
            [//Sem 2 Unit Objects
              {id: 'MGMT3000', name: 'E Man', credits: 25.0},
              {id: 'COMP3003', name: 'SE Concepts', credits: 25.0},
              {id: 'ISAD4001', name: 'SEP B', credits: 50.0}
            ]
          ]
        ]
}
