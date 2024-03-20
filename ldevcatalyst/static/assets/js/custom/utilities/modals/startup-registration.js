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
			var validator = validations[stepper.getCurrentStepIndex() - 1]; // get validator for currnt step

			if (validator) {
				validator.validate().then(function (status) {
					console.log(validator);
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
	}



	var handleForm = function() {
		formSubmitButton.addEventListener('click', function (e) {
			// Validate form before changing stepper step
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
					var founderInputs = founderNamesContainer.querySelectorAll(".founder-input-group");
					console.log(founderInputs);
					var foundersArray = [];
					founderInputs.forEach(function(inputGroup) {
						var founder = {
							name: inputGroup.querySelector(".founder-name-input").value,
							email: inputGroup.querySelector(".founder-email-input").value,
							mobile: inputGroup.querySelector(".founder-mobile-input").value,
							gender: inputGroup.querySelector(".founder-gender-input").value,
							linkedIn: inputGroup.querySelector(".founder-linkedin-input").value
						};
						foundersArray.push(founder);
					});
					console.log(foundersArray);
					formData.append("founder_names", JSON.stringify(foundersArray));
					$.ajax({
						url: actionUrl,
						type: 'POST',
						data: formData,
						processData: false,
						contentType: false,
						success: function (response) {
							// Always remove loading indication and enable button after submission
							formSubmitButton.removeAttribute('data-kt-indicator');
							formSubmitButton.disabled = false;
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
									formSubmitButton.removeAttribute('data-kt-indicator');
									formSubmitButton.disabled = false;
									stepperObj.goPrevious();
									stepperObj.goPrevious();
									KTUtil.scrollTop();
								});            
							}
						},
						error: function (xhr, status, error) {
							var errorMessage = "An error occurred while submitting the form. Please try again later.";
							if (xhr.responseJSON && xhr.responseJSON.error) {
								errorMessage = "Please fix the following error: " + xhr.responseJSON.error;
							}
							Swal.fire({
								text: errorMessage,
								icon: "error",
								buttonsStyling: false,
								confirmButtonText: "Ok, got it!",
								customClass: {
									confirmButton: "btn btn-light"
								}
							}).then(function () {
								formSubmitButton.removeAttribute('data-kt-indicator');
								formSubmitButton.disabled = false;
								stepperObj.goPrevious();
								stepperObj.goPrevious();
								KTUtil.scrollTop();
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
								message: 'Please enter statup name'
							}
						}
					},
                    co_founder_count: {
						validators: {
							notEmpty: {
								message: 'Please enter co founders count'
							}
						}
					},
					team_size: {
						validators: {
							notEmpty: {
								message: 'Please enter team size'
							}
						}
					},
                    market_size: {
						validators: {
							notEmpty: {
								message: 'Please enter market size'
							}
						}
					},
                    required_amount: {
						validators: {
							notEmpty: {
								message: 'Please enter required amount'
							}
						}
					},
					founding_year: {
						validators: {
							notEmpty: {
								message: 'Please select founding year'
							}
						}
					},
					founding_experience: {
						validators: {
							notEmpty: {
								message: 'Please select founding experience'
							}
						}
					},
					description: {
						validators: {
							notEmpty: {
								message: 'Please add description'
							}
						}
					},
					location_state: {
						validators: {
							notEmpty: {
								message: 'Please add state'
							}
						}
					},
					location_district: {
						validators: {
							notEmpty: {
								message: 'please add district  '
							}
						}
					},
					collaboration_sector: {
						validators: {
							notEmpty: {
								message: 'please add collaboration sector'
							}
						}
					},
					fundingfunding_stage_id_stage_id: {
						validators: {
							notEmpty: {
								message: 'please add funding stage number'
							}
						}
					}
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
					founder_names: {
						validators: {
							notEmpty: {
								message: 'Please enter founder names'
							}
						}
					},
					// poc_email: {
					// 	validators: {
					// 		notEmpty: {
					// 			message: 'Point of contact email is required'
					// 		},
					// 		emailAddress: {
					// 			message: 'Invalid email address'
					// 		}
					// 	}
					// },
					// poc_mobile: {
					// 	validators: {
					// 		notEmpty: {
					// 			message: 'Point of contact mobile number is required'
					// 		},
					// 		phone: {
					// 			country: function () {
					// 				return 'IN';
					// 			},
					// 			message: 'Invalid phone number'
					// 		}
					// 	}
					// },
					company_website: {
						validators: {
							notEmpty: {
								message: 'Company website is required'
							}
						}
					},
					video_link: {
						validators: {
							notEmpty: {
								message: 'Video link is required'
							}
						}
					},
					short_video_link: {
						validators: {
							notEmpty: {
								message: 'Short video link is required'
							}
						}
					},
					pitch_deck: {
						validators: {
							notEmpty: {
								message: 'Pitch deck is required'
							}
						}
					}
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
	}

	return {
		// Public Functions
		init: function () {
			// Elements
			modalEl = document.querySelector('#kt_modal_create_account');

			if ( modalEl ) {
				modal = new bootstrap.Modal(modalEl);	
			}					

			stepper = document.querySelector('#kt_create_account_stepper');

			if ( !stepper ) {
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
KTUtil.onDOMContentLoaded(function() {
    KTCreateAccount.init();
});