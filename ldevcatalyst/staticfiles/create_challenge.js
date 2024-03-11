$(document).ready(function () {
    // Add Beneficiary Formset
    $('#add-beneficiary').click(function () {
        var formset = $('#beneficiaries-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.beneficiary-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Requirement Formset
    $('#add-requirement').click(function () {
        var formset = $('#requirements-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.requirements-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Capability Formset
    $('#add-capability').click(function () {
        var formset = $('#capabilities-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.capabilities-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Outcome Formset
    $('#add-outcome').click(function () {
        var formset = $('#outcomes-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.outcomes-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Other Requirement Formset
    $('#add-other-requirement').click(function () {
        var formset = $('#other-requirements-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.other-requirements-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Objective Formset
    $('#add-objective').click(function () {
        var formset = $('#objectives-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.objectives-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Eligibility Criteria Formset
    $('#add-eligibility-criteria').click(function () {
        var formset = $('#eligibility-criteria-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.eligibility-criteria-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Evaluation Criteria Formset
    $('#add-evaluation-criteria').click(function () {
        var formset = $('#evaluation-criteria-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.evaluation-criteria-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Delete Formset
    $('.delete-formset').click(function () {
        var formset = $(this).closest('.formset');
        formset.remove();
    });
});
$(document).ready(function () {
    // Add Beneficiary Formset
    $('#add-beneficiary').click(function () {
        var formset = $('#beneficiaries-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.beneficiary-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Requirement Formset
    $('#add-requirement').click(function () {
        var formset = $('#requirements-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.requirements-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Capability Formset
    $('#add-capability').click(function () {
        var formset = $('#capabilities-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.capabilities-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Outcome Formset
    $('#add-outcome').click(function () {
        var formset = $('#outcomes-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.outcomes-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Other Requirement Formset
    $('#add-other-requirement').click(function () {
        var formset = $('#other-requirements-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.other-requirements-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Objective Formset
    $('#add-objective').click(function () {
        var formset = $('#objectives-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.objectives-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Eligibility Criteria Formset
    $('#add-eligibility-criteria').click(function () {
        var formset = $('#eligibility-criteria-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.eligibility-criteria-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Add Evaluation Criteria Formset
    $('#add-evaluation-criteria').click(function () {
        var formset = $('#evaluation-criteria-formset');
        var totalForms = formset.children().length;
        var newForm = formset.children('.evaluation-criteria-form:first').clone(true);
        newForm.find(':input').each(function () {
            var name = $(this).attr('name').replace('-0-', '-' + totalForms + '-');
            $(this).attr({'name': name, 'id': name}).val('');
        });
        formset.append(newForm);
    });

    // Delete Formset
    $('.delete-formset').click(function () {
        var formset = $(this).closest('.formset');
        formset.remove();
    });
});
