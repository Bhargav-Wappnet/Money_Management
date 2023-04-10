function validateFields() {
    var oldpassword = document.getElementById("oldpassword").value;
    var password = document.getElementById("password").value;
    var confirmpassword = document.getElementById("confirmpassword").value;

    var oldpassworderror = document.getElementById("oldpassword-error");
    var Passworderror = document.getElementById("password-error");
    var confirmpassworderror = document.getElementById("confirmpassword-error");

    // Retrieve the csrf token value from the hidden input field
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Reset error messages
    oldpassworderror.innerHTML = "";
    Passworderror.innerHTML = "";
    confirmpassworderror.innerHTML = "";

    // Validate form fields
    if (!oldpassword || !password || !confirmpassword) {
        if (!oldpassword) {
            oldpassworderror.innerHTML = "Old Password is required.";
        }
        if (!password) {
            Passworderror.innerHTML = "New Password is required.";
        }
        if (!confirmpassword) {
            confirmpassworderror.innerHTML = "Confirm Password is required.";
        }
    } else {
        // Validate password length
        if (password.length < 8) {
            Passworderror.innerHTML = "Password should be at least 8 characters long.";
        } else {
            // Validate password match
            if (password === oldpassword) {
                Passworderror.innerHTML = "Old password and new password cannot be the same.";
            } else if (password !== confirmpassword) {
                confirmpassworderror.innerHTML = "New password and confirm password do not match.";
            } else {
                // All fields are valid
                // Call the function to change password
                changePassword();
            }
        }
    }

}

function changePassword() {
    const form = document.querySelector("form");
    const data = new FormData(form);
    // Send a POST request to the server with the form data
    fetch('', {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(data => {
        // Check the success value in the response
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: 'success',
                text: 'Password Change Succesfully, Go and try again for signin.'
            }).then(() => {
                window.location.href = '/signin';
            });
        } else {
            // Display the error message using SweetAlert
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.message
            });
        }
    })
    .catch(error => {
        // Display the error message using SweetAlert
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'An error occurred while processing your request. Please try again later.'
        });
    });
}

document.getElementById("submitButton").addEventListener("click", function(event) {
    event.preventDefault();
    validateFields();
});
