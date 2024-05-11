from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import RollsRoyceProposal
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile

@login_required
def challenge_details(request):
    return render(request,'custom_ic/rolls_royce/details.html')

@login_required
def success_page(request):
    return render(request, 'custom_ic/rolls_royce/success.html')


@login_required
def error_page(request):
    return render(request, 'custom_ic/rolls_royce/error.html')



@login_required
def proposal_form(request):
    if request.method == 'POST':
        max_file_size  = 15 * 1024 * 1024  # 15MB
        proposed_rc_research_papers_files = request.FILES.get('proposed_rc_research_papers_files')
        supporting_documents = request.FILES.get('supporting_documents')

        user = request.user if request.user.is_authenticated else None
        form_data = {
            'user': user,
            'solution_name': request.POST.get('solution_name'),
            'focus_area': request.POST.get('focus_area'),
            'team_size': request.POST.get('team_size'),
            'team_composition': request.POST.get('team_composition'),
            'solution_brief': request.POST.get('solution_brief'),
            'solution_uniqueness': request.POST.get('solution_uniqueness'),
            'solution_sustainable_development_goals': request.POST.get('solution_sustainable_development_goals'),
            'innovation_current_stage': request.POST.get('innovation_current_stage'),
            'patent_status': request.POST.get('patent_status'),
            'proposed_rc_research_papers_exist': request.POST.get('proposed_rc_research_papers_exist'),
            'proposed_rc_research_papers_count': request.POST.get('proposed_rc_research_papers_count'),
            'proposed_rc_research_papers_links': request.POST.get('proposed_rc_research_papers_links'),
            'timeframe': request.POST.get('timeframe'),
            'expected_impacts_outcomes': request.POST.get('expected_impacts_outcomes'),
            'proposed_rc_research_papers_files' :request.FILES.get('proposed_rc_research_papers_files'),
            'supporting_documents' : request.FILES.get('supporting_documents')
        
        }
        errors = []
        if proposed_rc_research_papers_files:
            if isinstance(proposed_rc_research_papers_files, InMemoryUploadedFile) and proposed_rc_research_papers_files.size > max_file_size:
                errors.append("Research Papers file size should not exceed 15MB.")
            else:
                form_data['proposed_rc_research_papers_files'] = proposed_rc_research_papers_files

        if supporting_documents:
            if isinstance(supporting_documents, InMemoryUploadedFile) and supporting_documents.size > max_file_size:
                errors.append("Supporting Documents file size should not exceed 15MB.")
            else:
                form_data['supporting_documents'] = supporting_documents
        
        # Validate the form data
        try:
            proposed_rc_research_papers_count = form_data['proposed_rc_research_papers_count']
            proposed_rc_research_papers_count = int(proposed_rc_research_papers_count)
        except KeyError:
            pass
        except ValueError:
            errors.append("proposed research papers count should be numeric.")
        if not form_data['solution_name']:
            errors.append("Solution Name is required.")
        if not form_data['focus_area']:
            errors.append("Focus Area is required.")
        if not form_data['team_size']:
            errors.append("Team Size is required.")
        if not form_data['team_composition']:
            errors.append("Team Composition is required.")
        if not form_data['solution_brief']:
            errors.append("Solution Brief is required.")
        if not form_data['solution_uniqueness']:
            errors.append("Solution Uniqueness is required.")
        if not form_data['solution_sustainable_development_goals']:
            errors.append("Solution Sustainable Development Goals is required.")
        if not form_data['innovation_current_stage']:
            errors.append("Innovation Current Stage is required.")
        if not form_data['patent_status']:
            errors.append("Patent Status is required.")
        if not form_data['proposed_rc_research_papers_exist']:
            errors.append("Proposed RC Research Papers Exist is required.")
        if not form_data['timeframe']:
            errors.append("Timeframe is required.")
        if not form_data['expected_impacts_outcomes']:
            errors.append("Expected Impacts and Outcomes is required.")
        if proposed_rc_research_papers_files and isinstance(proposed_rc_research_papers_files, InMemoryUploadedFile) and proposed_rc_research_papers_files.size > max_file_size:
            errors.append("Research Papers file size should not exceed 5MB.")
        if supporting_documents and isinstance(supporting_documents, InMemoryUploadedFile) and supporting_documents.size > max_file_size:
            errors.append("Supporting Documents file size should not exceed 2MB.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'custom_ic/rolls_royce/proposal_form.html')
        
        proposal_form = RollsRoyceProposal.objects.create(**form_data)
        if proposal_form:
            messages.success(request, 'Proposal submitted successfully!')
            return redirect('rolls_royce_success_page')  
        else:
            messages.error(request, 'Error submitting proposal!')
            return redirect('rolls_royce_error_page')  
    return render(request, 'custom_ic/rolls_royce/proposal_form.html')



