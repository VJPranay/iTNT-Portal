"use strict";

// Class definition
var KTCreateAccount = function () {
    // Elements
    var modal;
    var modalEl;

    var stepper;
    var form;
    var formSubmitButton;
    var formContinueButton;
    var formPreviousButton;

    // Variables
    var stepperObj;
    var validations = [];

    // Private Functions
    var initStepper = function () {
        // Initialize Stepper
        stepperObj = new KTStepper(stepper);

        // Stepper change event
        stepperObj.on('kt.stepper.changed', function (stepper) {
            if (stepperObj.getCurrentStepIndex() === 2) {
                formSubmitButton.classList.remove('d-none');
                formSubmitButton.classList.add('d-inline-block');
                formContinueButton.classList.add('d-none');
            } else if (stepperObj.getCurrentStepIndex() === 3) {
                formSubmitButton.classList.add('d-none');
                formContinueButton.classList.add('d-none');
                formPreviousButton.classList.add('d-none');
            } else {
                formSubmitButton.classList.remove('d-inline-block');
                formSubmitButton.classList.remove('d-none');
                formContinueButton.classList.remove('d-none');
            }
        });

        // Validation before going to next page
        stepperObj.on('kt.stepper.next', function (stepper) {
            // Validate form before change stepper step
            var validator = validations[stepper.getCurrentStepIndex() - 1]; // get validator for current step
            if (validator) {
                validator.validate().then(function (status) {
                    if (status == 'Valid') {
                        stepper.goNext();
                        KTUtil.scrollTop();
                    } else {
                        Swal.fire({
                            text: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-light"
                            }
                        }).then(function () {
                            KTUtil.scrollTop();
                        });
                    }
                });
            } else {
                stepper.goNext();
                KTUtil.scrollTop();
            }
        });

        // Prev event
        stepperObj.on('kt.stepper.previous', function (stepper) {
            stepper.goPrevious();
            KTUtil.scrollTop();
        });
    };

    var handleForm = function () {
        formSubmitButton.addEventListener('click', function (e) {
            // Validate form before change stepper step
            var validator = validations[1]; // get validator for last form
            collectPatentsData();

            validator.validate().then(function (status) {
                if (status == 'Valid') {
                    // Prevent default button action
                    e.preventDefault();
                    
                    var formData = new FormData(form);
                    var actionUrl = form.getAttribute('action');

                    // Disable button to avoid multiple click 
                    formSubmitButton.disabled = true;

                    // Show loading indication
                    formSubmitButton.setAttribute('data-kt-indicator', 'on');

                    $.ajax({
                        url: actionUrl, // Use the action URL generated by {% url %}
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            if (response.success) {
                                // Optionally, display a success message
                                Swal.fire({
                                    text: "Form submitted successfully!",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-light"
                                    }
                                }).then(function () {
                                    formSubmitButton.removeAttribute('data-kt-indicator');
                                    formSubmitButton.disabled = false;
                                    formPreviousButton.disabled = false;
                                    stepperObj.goNext();
                                    var registrationIdDisplay = document.getElementById('registrationIdDisplay');
                                    registrationIdDisplay.innerText = response.registration_id;
                                });
                            } else {
                                Swal.fire({
                                    text: "An error occurred while submitting the form. Please try again later.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-light"
                                    }
                                }).then(function () {
                                    stepperObj.goPrevious();
                                    stepperObj.goPrevious();
                                    KTUtil.scrollTop();
                                    formSubmitButton.setAttribute('data-kt-indicator', 'off');
                                    formSubmitButton.disabled = false;
                                });
                            }
                        },
                        error: function (xhr, status, error) {
                            // Handle error response
                            // Show error message
                            Swal.fire({
                                text: "An error occurred while submitting the form. Please try again later.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-light"
                                }
                            });
                        }
                    });
                } else {
                    Swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-light"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

    };

    var initValidation = function () {
        // Step 1
        validations.push(FormValidation.formValidation(
            form,
            {
                fields: {
                    name: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your Full Name'
                            }
                        }
                    },
                    area_of_interest: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your Research Area...'
                            }
                        }
                    },
                    institution: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your Institution...'
                            }
                        }
                    },
                    department: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your Department..'
                            }
                        }
                    },
                    location_state: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your State...'
                            }
                        }
                    },
                    location_district: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your District... '
                            }
                        }
                    },
                    gender: {
                        validators: {
                            notEmpty: {
                                message: 'Please select your Gender... '
                            }
                        }
                    },
                    mobile: {
                        validators: {
                            notEmpty: {
                                message: 'Mobile number is required'
                            },
                            phone: {
                                country: function () {
                                    return 'IN';
                                },
                                message: 'Invalid phone number',
                            },
                        }
                    },
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Email is required'
                            },
                            emailAddress: {
                                message: 'The value is not a valid email address'
                            }
                        }
                    },
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
        ));

        // Step 2
        validations.push(FormValidation.formValidation(
            form,
            {
                fields: {
                    highest_qualification: {
                        validators: {
                            notEmpty: {
                                message: 'Please enter your Highest Qualification'
                            }
                        }
                    },
                    publication_title: {
                        validators: {
                            notEmptyIfPhD: {
                                message: 'Please enter Publication Title',
                                enabled: false // Initially disabled
                            }
                        }
                    },
                    paper_link: {
                        validators: {
                            notEmptyIfPhD: {
                                message: 'Please enter Paper Link',
                                enabled: false // Initially disabled
                            },
                            
                        }
                    },
                    journal: {
                        validators: {
                            notEmptyIfPhD: {
                                message: 'Please enter Journal',
                                enabled: false // Initially disabled
                            }
                        }
                    },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    // Bootstrap Framework Integration
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        
        ));

        // Step 3
        validations.push(FormValidation.formValidation(
            form,
            {
                fields: {

                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    // Bootstrap Framework Integration
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        ));


        FormValidation.validators.mandatoryIfPhD = {
            validate: function(input) {
                var highestQualification = form.querySelector('[name="highest_qualification"]').value.trim();
                // If highest_qualification is "Ph.D", the field should not be empty
                if (highestQualification === "Ph.D") {
                    return (input.value.trim() !== '');
                }
                // If highest_qualification is not "Ph.D", the field can be empty
                return true;
            }
        };
    };

    return {
        // Public Functions
        init: function () {
            // Elements
            modalEl = document.querySelector('#kt_modal_create_account');

            if (modalEl) {
                modal = new bootstrap.Modal(modalEl);
            }

            stepper = document.querySelector('#kt_create_account_stepper');

            if (!stepper) {
                return;
            }

            form = stepper.querySelector('#kt_create_account_form');
            formSubmitButton = stepper.querySelector('[data-kt-stepper-action="submit"]');
            formContinueButton = stepper.querySelector('[data-kt-stepper-action="next"]');
            formPreviousButton = stepper.querySelector('[data-kt-stepper-action="previous"]');

            initStepper();
            initValidation();
            handleForm();
        }
    };
}();


// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTCreateAccount.init();
});
