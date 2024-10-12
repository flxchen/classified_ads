//validates form
var form = document.getElementById("form");
var textarea = document.getElementById("body");
var submitButton = document.querySelector(
  'button[type="submit"].btn.btn-primary'
);

form.addEventListener(
  "submit",
  function (event) {
    event.preventDefault();    
    if (!form.checkValidity()) {
      form.classList.add("was-validated");
    } 
    else {
      if (confirm("Are you sure you want to post the ad?")) {
        process(submitButton);
        sendPhotosToServer();
        form.submit();              
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
function process(submitButton){  
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
  updateImageInput();console.log(uploadedPhotos);
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
async function sendPhotosToServer() {
  const formData = new FormData();
  
  // Append each photo from uploadedPhotos array to the form data
  uploadedPhotos.forEach((photo, index) => {
    formData.append(`photo_${index}`, photo);
  });
  console.log('category',category,'subcategory',subcategory,formData);
  try {
    const response = await fetch(`http://192.168.50.151:5000/post-ads/${category}/${subcategory}`, {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Photos uploaded successfully!",result);
    } else {
      console.log("Failed to upload photos.",response.status);
    }
  } catch (error) {
    console.error("Error during photo upload:", error);
    console.log("An error occurred while uploading photos.");
  }
}