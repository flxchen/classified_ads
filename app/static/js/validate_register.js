var form = document.getElementById("form");
//validate register form
form.addEventListener("submit", (e) => {
  e.preventDefault();
  var passwordMismatch = document.getElementById("passwordMismatch");
  var password = document.getElementById("new_password").value;
  var repeat_password = document.getElementById("repeat_password").value;
  console.log(password,repeat_password);
  if (!form.checkValidity()) {
    form.classList.add("was-validated");
  } else if (    
    !matchPassword(password, repeat_password)
  ) {    
    passwordMismatch.style.display = "block";
  } 
  else {
    form.submit();
  }
  //validate password matches
  function matchPassword(password, password2) {
    return password == password2;
  }
});
