function ValidateForm() {
  var clg = document.forms["form"]["college_code"].value;
  var branch = document.forms["form"]["branch_code"].value;
  var sem = document.forms["form"]["semester"].value;
  if ((clg == null || clg == "") && (branch == null || branch == "") && (sem == null || sem == "0")) {
    document.getElementById('x').innerHTML = '<div class="alert alert-error alert-danger"> ' +
    '<a href="#" class="close" data-dismiss="alert">&times;</a> ' +
    '<strong>Error!</strong> Please enter value in at least one field. ' +
    '</div>';
    return false;
  }

}