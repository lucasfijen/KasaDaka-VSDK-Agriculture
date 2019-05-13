from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from ..models import *

# class RegionSelection(TemplateView):

def region_options_resolve_redirect_urls(region_options, session):
    region_options_redirection_urls = []
    for region_option in region_options:
        redirect_url = region_option.redirect.get_absolute_url(session)
        region_options_redirection_urls.append(redirect_url)
    return region_options_redirection_urls

def region_options_resolve_voice_labels(region_options, language):
    """
    Returns a list of voice labels belonging to the provided list of choice_options.
    """
    region_options_voice_labels = []
    for region_option in region_options:
        region_options_voice_labels.append(region_option.get_voice_fragment_url(language))
    return region_options_voice_labels

def region_generate_context(region_element, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """
    region_options =  Region.objects.values_list('region_name', flat=True)
    language = get_object_or_404(Language, pk=2)
    context = {'region': region_element,
                'region_voice_label': region_options[region_name].get_voice_fragment_url(language),
                'region_options': region_options,
                'region_options_voice_labels': region_options_resolve_voice_labels(region_options, language),
                    'region_options_redirect_urls': region_options_resolve_redirect_urls(region_options, session),
                    'language': language, 
                    }
    return context

def region(request, session_id):
    region_element = get_list_or_404(Region)
    #regions = 
    print("hoi")
    print(region_element)
    session = get_object_or_404(CallSession, pk=session_id)
    #session.record_step(choice_element)
    context = region_generate_context(region_element, session)

    return render(request, 'region_selection.xml', context, content_type='text/xml')


def render_region_selection_form(request, session, redirect_url):
    regions = session.service.region.all()

    # This is the redirect URL to POST the region selected
    redirect_url_POST = reverse('service-development:region', args = [session.id])

    # This is the redirect URL for *AFTER* the region selection process
    pass_on_variables = {'redirect_url' : redirect_url}

    context = {'regions' : regions,
                'redirect_url' : redirect_url_POST,
                'pass_on_variables' : pass_on_variables
                }
    return render(request, 'region_selection.xml', context, content_type='text/xml')

# def get(self, request, session_id):
#     """
#     Asks the user to select one of the supported languages.
#     """
#     session = get_object_or_404(CallSession, pk = session_id)
#     voice_service = session.service
#     if 'redirect_url' in request.GET:
#         redirect_url = request.GET['redirect_url']
#     return self.render_region_selection_form(request, session, redirect_url)

def post(request, session_id):
    """
    Saves the chosen language to the session
    """
    if 'redirect_url' in request.POST:
        redirect_url = request.POST['redirect_url']
    else: raise ValueError('Incorrect request, redirect_url not set')
    if 'region_id' not in request.POST:
        raise ValueError('Incorrect request, region ID not set')

    session = get_object_or_404(CallSession, pk = session_id)
    voice_service = session.service
    region = get_object_or_404(Region, pk = request.POST['region_id'])

    session._region = region
    session.save()

    session.record_step(None, "Region selected, %s" % region.name)

    return HttpResponseRedirect(redirect_url)
