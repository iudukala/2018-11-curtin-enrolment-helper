/*********************************/
/*     DOM Element Variables     */
/*********************************/
var browseButton = document.getElementById('file-browse');
var fileInput = document.getElementById('file-input');
var uploadWidgetInner = document.getElementById('drag-target')
var errorMessageSpan = document.getElementById('error-text')

/*********************************/
/*      DOM Element Events       */
/*********************************/
//Button for selecting files
browseButton.onclick = function() {
  fileInput.click();
};

//Disable listener for dragging files onto all of the window
window.addEventListener("dragover",function(e){
  e.preventDefault();
},false);

/*********************************/
/*      GENERAL USE METHODS      */
/*********************************/
/*
 * Name: containsFile
 *
 * Purpose: Checks if a file is in a list of files
 *
 * Params: file: the file object to check for
 *         list: a list containing file objects
 *
 * Return: true if the file is found, false otherwise
 *
 * Notes: N/A
 */
function containsFile(file, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (sameFile(file, list[i])) {
            return true;
        }
    }
    return false;
}

/*
 * Name: sameFile
 *
 * Purpose: Checks if 2 files are 'identical'
 *
 * Params: x and y, 2 file objects
 *
 * Return: true if they're identical, false otherwise
 *
 * Notes: N/A
 */
function sameFile(x, y){
  return (x.name === y.name && x.size === y.size && x.type === y.type)
}

/*********************************/
/*       ANGULAR APP CODE        */
/*********************************/
var app = angular.module('uploadApp', []).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.controller('uploadCtrl', function($scope) {
  /**************************/
  /*  SCOPE INITIALIZATION  */
  /**************************/
  $scope.filelist = [];
  $scope.fileState = [];
  $scope.draggedover = false;
  $scope.filledFilelist = false;
  $scope.errorMessage = false;
  $scope.uploading = false;

  /*
   * Name: removeFile
   *
   * Purpose: Removes the specified file from the scope's file list
   *
   * Params: index, the index of the file to remove
   *
   * Return: N/A
   *
   * Notes: N/A
   */
  $scope.removeFile = function(index) {
    if(index > -1) {
      $scope.filelist.splice(index, 1);
      $scope.fileState.splice(index, 1);
      if($scope.filelist.length == 0){
        $scope.filledFilelist = false;
      }
    }
  };

  /*
   * Name: addFiles
   *
   * Purpose: Adds a set of files to the scope, provided they're not already present
   *
   * Params: inFiles, a file list object
   *
   * Return: N/A
   *
   * Notes: N/A
   */
  function addFiles(inFiles) {
    for(var i = 0; i < inFiles.length; i++) {
      if(inFiles[i].type != "application/pdf") {
        showErrorMessage("Non-PDF files entered, please only input PDF files.")
      }
      else if(!containsFile(inFiles[i], $scope.filelist)) {
        $scope.filelist.push(inFiles[i]);
        $scope.fileState.push('selecting');
      }
    }
    if($scope.filelist.length > 0){
      $scope.filledFilelist = true;
    }
    else {
      $scope.filledFilelist = false;
    }
    $scope.$apply();
    fileInput.value = "";
  }

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
   * Name: fileInput.onChange
   *
   * Purpose: Fires when the user selects a new set of files, and adds
   *          new files to the scope.
   *
   * Params: none
   *
   * Return: none
   *
   * Notes: N/A
   */
  fileInput.onchange = function() {
    addFiles(this.files)
  };

  /*
   * Name: uploadWidgetInner.ondrop
   *
   * Purpose: Handler for file input via drag and drop
   *
   * Params: e, The event object JS generates
   *
   * Return: none
   *
   * Notes: N/A
   */
   $scope.uploadFiles = function() {
     if($scope.filelist.length > 0) {
       $scope.uploading = true;
       for(var i = 0; i < $scope.filelist.length; i++) {
         $scope.fileState[i] = "uploading";
         setupAjaxRequest(i)
       }
     }
     else {
       showErrorMessage("Please input files before uploading.")
     }
   }

  /*
   * Name: setupAjaxRequest
   *
   * Purpose: Sets up an ajax request for each file being uploaded
   *
   * Params: fileIndex, the index of the file to be uploaded
   *
   * Return: none
   *
   * Notes: Randomly generates outcome for now, actual AJAX will be in future
   */
  //Endpoint: /pdfFileUpload
  function setupAjaxRequest(fileIndex) {
    var formData = new FormData();
    xhr = new XMLHttpRequest();

    //Setup formdata for file
    formData.append('file[]', $scope.filelist[fileIndex]);

    //Setup callback for request
    xhr.onload = function() {
      //Switch on status codes
      if(xhr.status === '200') {
        $scope.fileState[fileIndex] = 'success';
      }
      else {
        $scope.fileState[fileIndex] = 'failure';
      }

      if($scope.fileState.indexOf('uploading') < 0) {
        $scope.uploading = false;
      }
      $scope.$apply();
    };

    xhr.open('POST', '/pdfFileUpload');
    xhr.send(formData);
  }

  /*
   * Name: uploadWidgetInner.ondrop
   *
   * Purpose: Handler for file input via drag and drop
   *
   * Params: e, The event object JS generates
   *
   * Return: none
   *
   * Notes: N/A
   */
  uploadWidgetInner.ondrop = function(e) {
    e.preventDefault();
    addFiles(e.dataTransfer.files)
    $scope.draggedover = false;
    $scope.$apply();
  };

  uploadWidgetInner.ondragover = function() {
    $scope.draggedover = true;
    $scope.$apply();
  };

  uploadWidgetInner.ondragleave = function() {
    $scope.draggedover = false;
    $scope.$apply();
  };
});
