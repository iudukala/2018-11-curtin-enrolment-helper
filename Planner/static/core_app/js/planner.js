angular.module('plannerApp')
.controller('plannerCtrl', function($scope, $rootScope, StudentService) {
  //Keep track of student variable from other controller via the StudentService factory
  $scope.theStudent = {};
  $scope.theJSON = parsedJSON;
  $scope.tableWidth = document.getElementById('template-table').clientWidth;
  $scope.$watch(function () { return StudentService.getStudent(); }, function (newValue, oldValue) {
    if (newValue !== oldValue) $scope.theStudent = newValue;
  });

  //Back button
  $scope.backToStudents = function() {
    $rootScope.selectingStudent = true;
  }

  $scope.cellStyle = function(status, credits) {
    var style = {}
    if(credits === 12.5) {
      style['width'] = '11%';
      style['font-size'] = '12px';
    }
    else if(credits === 50.0) {
      style['width'] = '44%';
    }
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






















/***********************************************************************************************************
//TEST DATA ONLY
var receivedJSON = {
  course: { name: 'Computer Science Stream', id: 'STRU-CMPSC' },
  template: {
              1 : {
                    1 : {
                      COMP1001 : { name: 'Y1S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1002 : { name: 'Y1S1U2', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1003 : { name: 'Y1S1U3', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1004 : { name: 'Y1S1U4', credits: 25.0, status: 'PASS', attempts: 1}
                    },
                    2: {
                      COMP1005 : { name: 'Y1S2U1', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1006 : { name: 'Y1S2U2', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1007 : { name: 'Y1S2U3', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP1008 : { name: 'Y1S2U4', credits: 25.0, status: 'PASS', attempts: 1}
                    }
                  },
              2 : {
                    1 : {
                      COMP2001 : { name: 'Y2S1U1', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2002 : { name: 'Y2S1U2', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2003 : { name: 'Y2S1U3', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2004 : { name: 'Y2S1U4', credits: 25.0, status: 'PASS', attempts: 1}
                    },
                    2: {
                      COMP2005 : { name: 'Y2S2U1', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2006 : { name: 'Y2S2U2', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2007 : { name: 'Y2S2U3', credits: 25.0, status: 'PASS', attempts: 1},
                      COMP2008 : { name: 'Y2S2U4', credits: 25.0, status: 'PASS', attempts: 1}
                    }
                  },
              3 : {
                    1 : {
                      COMP3001 : { name: 'Y3S1U1', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3002 : { name: 'Y3S1U2', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3003 : { name: 'Y3S1U3', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3004 : { name: 'Y3S1U4', credits: 25.0, status: 'PLN', attempts: 1}
                    },
                    2: {
                      COMP3005 : { name: 'Y3S2U1', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3006 : { name: 'Y3S2U2', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3007 : { name: 'Y3S2U3', credits: 25.0, status: 'PLN', attempts: 1},
                      COMP3008 : { name: 'Y3S2U4', credits: 25.0, status: 'PLN', attempts: 1}
                    }
                  },
            },
  plan: { }
}
***********************************************************************************************************/
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
                  {id: 'COMP3007', name: 'Y3S2U3', credits: 50.0, status: 'PLN', attempts: 0}
                ]
              ]
            ],
  plan: [//Array of years
          [//Year 1
            [//Sem 1 Unit Objects
              {id: 'COMP3001', name: 'Y3S1U1', credits: 25.0},
              {id: 'COMP3002', name: 'Y3S1U2', credits: 25.0},
              {id: 'COMP3003', name: 'Y3S1U3', credits: 25.0},
              {id: 'COMP3004', name: 'Y3S1U4', credits: 25.0},
            ],
            [//Sem 2 Unit Objects
              {id: 'COMP3005', name: 'Y3S2U1', credits: 25.0},
              {id: 'COMP3006', name: 'Y3S2U2', credits: 25.0},
              {id: 'COMP3007', name: 'Y3S2U3', credits: 25.0},
              {id: 'COMP3008', name: 'Y3S2U4', credits: 25.0},
            ]
          ]
        ]
}
