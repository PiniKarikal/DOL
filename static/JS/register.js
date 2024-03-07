const checkbox = document.getElementById('myCheckbox');
    const button = document.getElementById('myButton');
    const form = document.getElementById('registrationForm');

    checkbox.addEventListener('change', function() {
      if (button.disabled = !this.checked) {
        button.style.border = "1px solid rgb(0, 0, 128)"
        button.style.color = "grey"
    } else {
        button.style.border = "2px solid rgb(0, 0, 128)"
        button.style.color = "rgb(0, 0, 128)"
      }
    });


    form.addEventListener('submit', function(event) {
        // Uncheck the checkbox after submission
        checkbox.checked = false;
      });
    