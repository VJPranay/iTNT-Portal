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
							html: "<strong>We noticed some errors in your form. Please review the information you entered, make any necessary corrections, and then resubmit the form.</strong>",
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
	}

	var handleForm = function() {
		formSubmitButton.addEventListener('click', function (e) {
			// Validate form before change stepper step
			var validator = validations[1]; // get validator for last form

			validator.validate().then(function (status) {
				if (status == 'Valid') {
					// Prevent default button action
					e.preventDefault();
					var formData = new FormData(form);
					var actionUrl = form.getAttribute('action');

					// Disable button to avoid multiple clicks 
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
								var errorMessages = getErrorMessages(response.error);
								Swal.fire({
									html: "<strong>Please fix the following errors before submitting the form:</strong><ul>" + errorMessages + "</ul>",
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
									formSubmitButton.disabled = false;
									formSubmitButton.setAttribute('data-kt-indicator', 'off');
								});			
							}
						},
						error: function (xhr, status, error) {
							// Handle error response
							Swal.fire({
								text: "We noticed some errors in your form. Please review the information you entered, make any necessary corrections, and then resubmit the form.",
								icon: "error",
								buttonsStyling: false,
								confirmButtonText: "Ok, got it!",
								customClass: {
									confirmButton: "btn btn-light"
								}
							});
							formSubmitButton.disabled = false;
							formSubmitButton.setAttribute('data-kt-indicator', 'off');
						}
					});
				} else {
					Swal.fire({
						text: "We noticed some errors in your form. Please review the information you entered, make any necessary corrections, and then resubmit the form.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "Ok, got it!",
						customClass: {
							confirmButton: "btn btn-light"
						}
					}).then(function () {
						formSubmitButton.disabled = false;
						formSubmitButton.setAttribute('data-kt-indicator', 'off');
						KTUtil.scrollTop();
					});
				}
			});
		});
	}

	var getErrorMessages = function(errors) {
		var messages = [];
		for (var field in errors) {
			if (errors.hasOwnProperty(field)) {
				messages.push('<li>' + field + ": " + errors[field].join(', ') + '</li>');
			}
		}
		return messages.join('');
	}

	var initValidation = function () {
		// Step 1
		validations.push(FormValidation.formValidation(
			form,
			{
				fields: {
					name: {
						validators: {
							notEmpty: {
								message: 'Please enter your name'
							}
						}
					},
					institution: {
						validators: {
							notEmpty: {
								message: 'Please select Institution'
							}
						}
					},
					department: {
						validators: {
							notEmpty: {
								message: 'Please select your department'
							}
						}
					},
					year_of_graduation: {
						validators: {
							notEmpty: {
								message: 'Enter year of Graduation'
							}
						}
					},
					location_state: {
						validators: {
							notEmpty: {
								message: 'Please select your State'
							}
						}
					},
					location_district: {
						validators: {
							notEmpty: {
								message: 'Please select your District'
							}
						}
					},
					collaboration_sector: {
						validators: {
							notEmpty: {
								message: 'Area of collaboration is required'
							}
						}
					},
					poc_email: {
						validators: {
							notEmpty: {
								message: 'Point of contact email is required'
							},
							emailAddress: {
								message: 'Invalid email address',
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
					project_idea: {
						validators: {
							notEmpty: {
								message: 'Enter your Project details'
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

		// Step 3
		validations.push(FormValidation.formValidation(
			form,
			{
				fields: {
					// Add any additional field validations for Step 3 here
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
	}

	return {
		// Public Functions
		init: function () {
			// Elements
			modalEl = document.querySelector('#kt_modal_create_account');
			if (!modalEl) {
				return;
			}

			modal = new bootstrap.Modal(modalEl);

			stepper = document.querySelector('#kt_create_account_stepper');
			form = document.querySelector('#kt_create_account_form');
			formSubmitButton = document.querySelector('[data-kt-stepper-action="submit"]');
			formContinueButton = document.querySelector('[data-kt-stepper-action="next"]');
			formPreviousButton = document.querySelector('[data-kt-stepper-action="previous"]');

			initStepper();
			initValidation();
			handleForm();
		}
	};
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
	KTCreateAccount.init();
});

