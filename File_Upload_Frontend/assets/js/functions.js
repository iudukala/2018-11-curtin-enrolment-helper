/*********************************/
/*     DOM Element Variables     */
/*********************************/
var browseButton = document.getElementById('file-browse');
var fileInput = document.getElementById('file-input');

/*********************************/
/*      DOM Element Events       */
/*********************************/
browseButton.onclick = function() {
  fileInput.click();
};

/*********************************/
/*      GENERAL USE METHODS      */
/*********************************/
/*
 * Name: containsObject
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

  /*
   * Name: removeFile
   *
   * Purpose: Removes the specified file from the scope's file list
   *
   * Params: file, the file object to remove
   *
   * Return: N/A
   *
   * Notes: N/A
   */
  $rootScope.removeFile = function(file) {
    var index = $rootScope.filelist.indexOf(file);
    $rootScope.filelist.splice(index, 1);
    console.log($rootScope.filelist)
  };

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
    for(var i = 0; i < this.files.length; i++) {
      if(!containsFile(this.files[i], $rootScope.filelist)) {
        $rootScope.filelist.push(this.files[i]);
      }
    }
    $rootScope.$apply();
    console.log($rootScope.filelist)
    fileInput.value = "";
  };

  //Finally, apply the scope and let the magic happen!
  $rootScope.$apply();
});
