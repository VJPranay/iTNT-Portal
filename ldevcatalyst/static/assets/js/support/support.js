// Class definition
var SupportModal = function () {
	var submitButton;
	var cancelButton;
	var validator;
	var form;
	var modal;
	var modalEl;

	// Init form inputs
	var initForm = function() {
		// Team assign. For more info, please visit the official plugin site: https://select2.org/
        $(form.querySelector('[name="category"]')).on('change', function() {
            // Revalidate the field when an option is chosen
            validator.revalidateField('category');
        });
	}

	// Handle form validation and submission
	var handleForm = function() {
		// Init form validation rules. For more info check the FormValidation plugin's official documentation: https://formvalidation.io/
		validator = FormValidation.formValidation(
			form,
			{
				fields: {
					'name': {
						validators: {
							notEmpty: {
								message: 'Your name is required'
							}
						}
					},
					'email': {
						validators: {
							notEmpty: {
								message: 'Your email is required'
							}
						}
					},
					'mobile': {
						validators: {
							notEmpty: {
								message: 'Your mobile is required'
							}
						}
					},
					'account_role': {
						validators: {
							notEmpty: {
								message: 'Account role is required'
							}
						}
					},
					'support_category': {
						validators: {
							notEmpty: {
								message: 'Please choose your support category'
							}
						}
					},
					'short_description': {
						validators: {
							notEmpty: {
								message: 'Short description is required'
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
		);

		// Action buttons
		submitButton.addEventListener('click', function (e) {
			e.preventDefault();

			// Validate form before submit
			if (validator) {
				validator.validate().then(function (status) {
					if (status == 'Valid') {
						submitButton.setAttribute('data-kt-indicator', 'on');
						submitButton.disabled = true;

						// AJAX request to submit form data
						$.ajax({
							type: 'POST',
							url: form.getAttribute('form-data-url'),
							data: $(form).serialize(),
							success: function(response) {
								if (response.success) {
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
								} else {
									Swal.fire({
										text: "Form submission failed. Please try again.",
										icon: "error",
										buttonsStyling: false,
										confirmButtonText: "Ok, got it!",
										customClass: {
											confirmButton: "btn btn-primary"
										}
									});
								}
							},
							error: function(xhr, status, error) {
								console.error('Error:', error);
							},
							complete: function() {
								submitButton.removeAttribute('data-kt-indicator');
								submitButton.disabled = false;
							}
						});                   
					} else {
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
				text: "Are you sure you would like to cancel?",
				icon: "warning",
				showCancelButton: true,
				buttonsStyling: false,
				confirmButtonText: "Yes, cancel it!",
				cancelButtonText: "No, return",
				customClass: {
					confirmButton: "btn btn-primary",
					cancelButton: "btn btn-active-light"
				}
			}).then(function (result) {
				if (result.value) {
					form.reset();
					modal.hide();
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
	}

	return {
		// Public functions
		init: function () {
			modalEl = document.querySelector('#support_modal');

			if (!modalEl) {
				return;
			}

			modal = new bootstrap.Modal(modalEl);

			form = document.querySelector('#support_modal_form');
			submitButton = document.getElementById('support_modal_submit');
			cancelButton = document.getElementById('support_modal_cancel');

			initForm();
			handleForm();
		}
	};
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
	SupportModal.init();
});
