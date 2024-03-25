// Class definition
var KTModalNewAddress = function () {
    var submitButton;
    var cancelButton;
    var validator;
    var form;
    var modal;
    var modalEl;

    
    // Function to make a POST request
    var fetchStartupDetails = function(startupId) {
        // Prepare data for the POST request
        const data = {
            startup_id: startupId
        };

        // Options for the fetch request
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Assuming you have a function to retrieve CSRF token from cookies
            },
            body: JSON.stringify(data)
        };
			// Access the anchor tag element
			var anchorTag = document.querySelector('[data-bs-target="#kt_modal_new_address"]');

			// Get the value of the data-fetch-url attribute
			var fetchUrl = anchorTag.getAttribute('data-fetch-url');

			// Make the fetch request
			fetch(fetchUrl, options).then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response data as needed
                console.log(data);
                console.log(data.html);
                // Inject the HTML received into the modal content
                document.getElementById('startup_profile_data').innerHTML = data.html;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };

    // Handle form validation and submission
    var handleForm = function() {
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );

        // Action buttons
        submitButton.addEventListener('click', function (e) {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    console.log('validated!');

                    if (status == 'Valid') {
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable button to avoid multiple clicks 
                        submitButton.disabled = true;

                        // Simulate ajax process
                        setTimeout(function() {
                            submitButton.removeAttribute('data-kt-indicator');

                            // Enable button
                            submitButton.disabled = false;
                            
                            // Show success message.  For more info check the plugin's official documentation: https://sweetalert2.github.io/
                            Swal.fire({
                                text: "Form has been successfully submitted!",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            }).then(function (result) {
                                if (result.isConfirmed) {
                                    modal.hide();
                                }
                            });

                            //form.submit(); // Submit form
                        }, 2000);                           
                    } else {
                        // Show error message.
                        Swal.fire({
                            text: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });

        cancelButton.addEventListener('click', function (e) {
            e.preventDefault();

            Swal.fire({
                text: "Do you really want to close this??",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: "Yes, close it!",
                cancelButtonText: "No, return",
                customClass: {
                    confirmButton: "btn btn-primary",
                    cancelButton: "btn btn-active-light"
                }
            }).then(function (result) {
                if (result.value) {
                    form.reset(); // Reset form    
                    modal.hide(); // Hide modal                
                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Your form has not been cancelled!.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary",
                        }
                    });
                }
            });
        });
    };

    // Function to get CSRF token from cookies
    var getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    return {
        // Public functions
        init: function () {
            // Elements
            modalEl = document.querySelector('#kt_modal_new_address');

            if (!modalEl) {
                return;
            }

            modal = new bootstrap.Modal(modalEl);

            form = document.querySelector('#kt_modal_new_address_form');
            submitButton = document.getElementById('kt_modal_new_address_submit');
            cancelButton = document.getElementById('kt_modal_new_address_cancel');

            // Handle form validation and submission
            handleForm();

            // Open modal event listener
            modalEl.addEventListener('show.bs.modal', function (event) {
                // Get the startup ID from the data attribute
                var anchorTag = event.relatedTarget;
                var startupId = anchorTag.getAttribute('data-startup-id');

                // Make a POST request to fetch startup details
                fetchStartupDetails(startupId);
                console.log(startupId);
            });
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTModalNewAddress.init();
});
