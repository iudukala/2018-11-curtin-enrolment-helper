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
    //Uncomment when merging
    //$http.get('/url').then(studentListHandler, studentSelectErrorHandler);
    $rootScope.openSpinner('Loading student list...');
    setTimeout(studentListHandler, 1000);
  };
  //Invoke this method while controller is loading
  getStudentList();

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
  function studentListHandler(/*response*/) {
    //var json = response.data;

    /*TEST DATA*/
    $scope.students =  [{ 'id': '16171921', 'name': 'Campbell Pedersen'},
                        { 'id': '16365481', 'name': 'Chung-Yen Lu'},
                        { 'id': '16102183', 'name': 'Chen Bi'},
                        { 'id': '17080170', 'name': 'Yoakim Persson'},
                        { 'id': '17898755', 'name': 'Thien Quang Trinh'},
                        { 'id': '17160182', 'name': 'Scott Ryan Day'},
                        { 'id': '17420420', 'name': 'Ash Tulett'},
                        { 'id': '16685281', 'name': 'Tim Cochrane'},
                        { 'id': '16402918', 'name': 'Jordan Van-Elden'},
                        { 'id': '17281204', 'name': 'Aidan Noël Jolly'},
                        { 'id': '69420420', 'name': 'Sam "Trek" Barker'}];
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
      //Uncomment when merging
      //$http.get('/getStudentList').then(templateHandler, studentSelectErrorHandler);
      $rootScope.openSpinner('Fetching student template...');
      templateHandler(parsedJSON)
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
    //var json = response.data;
    StudentService.setJSON(parsedJSON);
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
var parsedJSON = {
  course: { name: 'Computer Science Stream', id: 'STRU-CMPSC' },
  template: [//Array of years
              [//Year 1
                [//Sem 1 Unit Objects
                  {id: 'COMP1001', name: 'Y1S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1002', name: 'Y1S1U2', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1003', name: 'Y1S1U3', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1004', name: 'Y1S1U4', credits: 25.0, status: 'PASS', attempts: 1},
                ],
                [//Sem 2 Unit Objects
                  {id: 'COMP1001', name: 'Y1S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1001', name: 'Y1S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1007', name: 'Y1S2U3', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP1008', name: 'Y1S2U4', credits: 12.5, status: 'PASS', attempts: 1},
                  {id: 'COMP1009', name: 'Y1S2U5', credits: 12.5, status: 'PASS', attempts: 1}
                ]
              ],
              [//Year 2
                [//Sem 1 Unit Objects
                  {id: 'COMP2001', name: 'Y2S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2002', name: 'Y2S1U2', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2003', name: 'Y2S1U3', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2004', name: 'Y2S1U4', credits: 25.0, status: 'PASS', attempts: 1},
                ],
                [//Sem 2 Unit Objects
                  {id: 'COMP2005', name: 'Y2S2U1', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2006', name: 'Y2S2U2', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2007', name: 'Y2S2U3', credits: 25.0, status: 'PASS', attempts: 1},
                  {id: 'COMP2008', name: 'Y2S2U4', credits: 25.0, status: 'PASS', attempts: 1},
                ]
              ],
              [//Year 3
                [//Sem 1 Unit Objects
                  {id: 'COMP3001', name: 'Y3S1U1', credits: 25.0, status: 'PLN', attempts: 1},
                  {id: 'COMP3002', name: 'Y3S1U2', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP3003', name: 'Y3S1U3', credits: 50.0, status: 'PLN', attempts: 0}
                ],
                [//Sem 2 Unit Objects
                  {id: 'COMP3005', name: 'Y3S2U1', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP3006', name: 'Y3S2U2', credits: 25.0, status: 'PLN', attempts: 0},
                  {id: 'COMP3007', name: 'Y3S2U3', credits: 50.0, status: 'PLN', attempts: 0},
                ]
              ]
            ],
  plan: [//Array of years
          [//Year 1
            [//Sem 1 Unit Objects
              {id: 'COMP3001', name: 'Y3S1U1', credits: 25.0},
              {id: 'COMP3002', name: 'Y3S1U2', credits: 25.0},
              {id: 'COMP3003', name: 'Y3S1U3', credits: 50.0}
            ],
            [//Sem 2 Unit Objects
              {id: 'COMP3005', name: 'Y3S2U1', credits: 25.0},
              {id: 'COMP3006', name: 'Y3S2U2', credits: 25.0},
              {id: 'COMP3007', name: 'Y3S2U3', credits: 50.0}
            ]
          ]
        ]
}
