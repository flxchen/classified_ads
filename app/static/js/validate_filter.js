// validate filter options
var form = document.getElementById("form");
var submitButton = document.querySelector(
  'button[type="submit"].btn.btn-primary'
);
form.addEventListener("submit", (e) => {
  e.preventDefault();  
  if (!form.checkValidity()) {
    form.classList.add("was-validated");
  } 
  else {
    process(submitButton);
    form.submit();
  }
});
// Disable the button and add spinner
function process(submitButton){  
  submitButton.disabled = true;
  submitButton.innerHTML = `
  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...`;
}