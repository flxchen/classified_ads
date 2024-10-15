//validates form
var form = document.getElementById("form");
var textarea = document.getElementById("body");
var submitButton = document.getElementById("submit-button");

form.addEventListener(
  "submit",
  function (event) {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.classList.add("was-validated");
    } else {
      if (confirm("Are you sure you want to post the ad?")) {
        process(submitButton);
        sendFormToServer();
      }
    }
  },
  false
);
//set textarea validity based on input
textarea.addEventListener("input", function () {
  if (isValidInput(this.value)) {
    this.setCustomValidity("");
  } else {
    this.setCustomValidity("Invalid input");
  }
});

//ensure body is at least 12 characters
function isValidInput(value) {
  return value.trim().length >= 12;
}

// Disable the button and add spinner
function process(submitButton) {
  submitButton.disabled = true;
  submitButton.innerHTML = `
  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...`;
}

//handle pictures uploading
const imageInput = document.getElementById("formFileMultiple");
const output = document.querySelector("#result");
let total = 0;
const max_file_number = 6;
const uploadedPhotos = [];
imageInput.addEventListener("change", handleImageUpload);

function handleImageUpload(e) {
  const files = Array.from(e.target.files);
  const number_of_images = files.length;
  const remainingSlots = max_file_number - total;

  for (let i = 0; i < Math.min(number_of_images, remainingSlots); i++) {
    if (!files[i].type.startsWith("image/")) {
      alert(`File ${files[i].name} is not an image.`);
      continue;
    }
    if (files[i].size > 4 * 1024 * 1024) {
      alert(`File ${files[i].name} exceeds the 4MB size limit.`);
      continue;
    }
    uploadedPhotos.push(files[i]);
    const picReader = new FileReader();
    picReader.addEventListener("load", (event) => {
      const imgContainer = document.createElement("div");
      imgContainer.className = "col";
      imgContainer.innerHTML = `<div class="card">
                            <div class="image-container">
                                <img src="${event.target.result}" alt="${files[i].name}" class="card-img-top" style="height: 200px;
  object-fit: cover;">
                            </div>
                            <div class="card-body">
                                <button class="btn btn-danger btn-sm delete-btn">Delete</button>
                            </div>
                        </div>
                    `;
      const deleteBtn = imgContainer.querySelector(".delete-btn");
      deleteBtn.addEventListener("click", () => {
        imgContainer.remove();
        total--;
        const index = uploadedPhotos.indexOf(files[i]);
        if (index > -1) {
          uploadedPhotos.splice(index, 1); // Remove the file from the array
        }        
        updateImageInput();
      });
      total++;
      output.appendChild(imgContainer);
      updateImageInput();
    });
    picReader.readAsDataURL(files[i]);
  }
  updateImageInput();  
}
//check max photo limit
function updateImageInput() {
  if (total >= max_file_number) {
    imageInput.disabled = true;
    alert(`maximum ${max_file_number} photos reached!`);
  } else {
    imageInput.disabled = false;
  }
}

// Function to send the uploaded photos to the Flask endpoint
async function sendFormToServer() {
  const formData = new FormData();
  console.log(uploadedPhotos);
  // Append each photo from uploadedPhotos array to the form data
  uploadedPhotos.forEach((photo) => {
    formData.append("uploaded_photo", photo);
  });
  const subject = document.getElementById("subject").value;
  const city = document.getElementById("city").value;
  const state = document.getElementById("state").value;
  const address = document.getElementById("address").value;
  const zipcode = document.getElementById("zip-code").value;
  const body = document.getElementById("body").value;
  const email = document.getElementById("email").value;
  var phone = document.getElementById("phone");
  if (phone) {
    phone = phone.value;
  }
  var bedroom = document.getElementById("bedroom");
  if (bedroom) {
    bedroom = bedroom.value;
  }
  var bathroom = document.getElementById("bathroom");
  if (bathroom) {
    bathroom = bathroom.value;
  }
  var size = document.getElementById("size");
  if (size) {
    size = size.value;
  }
  var type = document.getElementById("Options");
  if (type) {
    type = type.value;
  }
  var rent = document.getElementById("rent");
  if (rent) {
    rent = rent.value;
  }
  var period = document.getElementById("period");
  if (period) {
    period = period.value;
  }
  var price = document.getElementById("price");
  if (price) {
    price = price.value;
  }
  var mileage = document.getElementById("mileage");
  if(mileage == undefined){mileage = ""}
  if (mileage) {
    mileage = mileage.value;
  }
  var brand = document.getElementById("brand");
  if (brand) {
    brand = brand.value;
  }  
  var make = document.getElementById("make");
  if (make) {
    make = make.value;
  }
  var model = document.getElementById("model");
  if (model) {
    model = model.value;
  }
  var condition = document.getElementById("condition");
  if (condition) {
    condition = condition.value;
  }
  var industry = document.getElementById("industry");
  if (industry) {
    industry = industry.value;
  }
  var compensation = document.getElementById("compensation");
  if (compensation) {
    compensation = compensation.value;
  }

  formData.append("subject", subject);
  formData.append("city", city);
  formData.append("state", state);
  formData.append("address", address);
  formData.append("zip-code", zipcode);
  formData.append("body", body);
  formData.append("phone", phone);
  formData.append("email", email);
  formData.append("bedroom", bedroom);
  formData.append("bathroom", bathroom);
  formData.append("size", size);
  formData.append("type", type);
  formData.append("rent", rent);
  formData.append("period", period);
  formData.append("price", price);
  formData.append("mileage", mileage);
  formData.append("brand", brand);
  formData.append("make", make);
  formData.append("model", model);
  formData.append("condition", condition);
  formData.append("industry", industry);
  formData.append("compensation", compensation);
  
  try {
    const response = await fetch(`/post-ads/${category}/${subcategory}`, {
      method: "POST",
      body: formData,
    })
    if (response.ok) {
      const server_response = await response.json();
      if (server_response.success) {
        // Redirect the user manually to the new location
        window.location.href = '/donate';
      }
      console.log("Photos uploaded successfully!");
    } else {
      console.log("Failed to upload photos.", response.status);
    }
  } catch (error) {
    console.error("Error during photo upload:", error);
    console.log("An error occurred while uploading photos.");
  }
}
