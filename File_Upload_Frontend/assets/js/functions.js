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
var app = angular.module('uploadApp', []);
app.controller('uploadCtrl', function($scope) {
});
app.run(function($rootScope) {
  /**************************/
  /*  SCOPE INITIALIZATION  */
  /**************************/
  $rootScope.filelist = [];
  $rootScope.fileState = [];
  $rootScope.draggedover = false;
  $rootScope.filledFilelist = false;
  $rootScope.errorMessage = false;
  $rootScope.uploading = false;

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
  $rootScope.removeFile = function(index) {
    if(index > -1) {
      $rootScope.filelist.splice(index, 1);
      $rootScope.fileState.splice(index, 1);
      if($rootScope.filelist.length == 0){
        $rootScope.filledFilelist = false;
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
      else if(!containsFile(inFiles[i], $rootScope.filelist)) {
        $rootScope.filelist.push(inFiles[i]);
        $rootScope.fileState.push('selecting');
      }
    }
    if($rootScope.filelist.length > 0){
      $rootScope.filledFilelist = true;
    }
    else {
      $rootScope.filledFilelist = false;
    }
    $rootScope.$apply();
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
    $rootScope.errorText = inputMessage
    $rootScope.errorMessage = true;
    setTimeout(function() {
      $rootScope.errorMessage = false;
      $rootScope.$apply();
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
   $rootScope.uploadFiles = function() {
     if($rootScope.filelist.length > 0) {
       $rootScope.uploading = true;
       for(var i = 0; i < $rootScope.filelist.length; i++) {
         $rootScope.fileState[i] = "uploading";
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
   function setupAjaxRequest(fileIndex) {
     setTimeout(function(){
       if(1) {//Math.random() >= 0.5) {
         $rootScope.fileState[fileIndex] = "success";
       }
       else {
         $rootScope.fileState[fileIndex] = "failure";
       }
       if($rootScope.fileState.indexOf("uploading") < 0) {
         $rootScope.uploading = false;
       }
       $rootScope.$apply();
     }, Math.floor(Math.random() * 6000) + 2000);
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
    $rootScope.draggedover = false;
    $rootScope.$apply();
  };

  uploadWidgetInner.ondragover = function() {
    $rootScope.draggedover = true;
    $rootScope.$apply();
  };

  uploadWidgetInner.ondragleave = function() {
    $rootScope.draggedover = false;
    $rootScope.$apply();
  };

  //Finally, apply the scope and let the magic happen!
  $rootScope.$apply();
});
