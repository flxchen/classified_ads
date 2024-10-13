fetch("/home", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.text())
    .then((data) => {
      alert(data); // Display the server response
      photoList.length = 0; // Clear the photo list after submission
      displayPhotos(); // Update the displayed list
    })
    .catch((error) => console.error("Error:", error));