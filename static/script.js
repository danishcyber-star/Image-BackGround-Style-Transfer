
  // Function to display the content image
  function displayContentImage(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var img = document.getElementById("content-image-preview");
        img.src = e.target.result;
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

  // Function to display the style image
  function displayStyleImage(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var img = document.getElementById("style-image-preview");
        img.src = e.target.result;
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

  // Function to submit the form
  function submitForm() {
    var contentImage = document.getElementById("content-image").files[0];
    var styleImage = document.getElementById("style-image").files[0];
    var formData = new FormData();
    formData.append("content_image", contentImage);
    formData.append("style_image", styleImage);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{{ url_for('stylize_image') }}");
    xhr.send(formData);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          var stylizedImage = document.getElementById("stylized-image-preview");
          stylizedImage.src = response.stylized_image_url;
        }
      }
    };
  }

