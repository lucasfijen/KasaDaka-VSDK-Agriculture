from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from ..models import *

# def region_generate_context(session):
    
#     regions = get_list_or_404(Region)
#     region_options =  Region.objects.values_list('region_name', flat=True)
#     language = get_object_or_404(Language, pk=2)
#     context = {'region': regions,
#                 'region_voice_labels': [region_name.voice_label.get_voice_fragment_url(language) for region_name in regions],
#                 'region_options': region_options,
#                 'region_options_redirect_urls': ['vxml/region_redirect/' + str(region_options[n]) for n, _ in enumerate(regions, 0)],
#                 'language': language
#                     }
#     return context

# def region(request, session_id):
#     #region_element = get_list_or_404(Region)
#     region_options =  Region.objects.values_list('region_name', flat=True)
#     print("hoi")
#     print(region_options[1])
#     session = get_object_or_404(CallSession, pk=session_id)
#     #session.record_step(choice_element)
#     context = region_generate_context(session)

#     return render(request, 'region_selection.xml', context, content_type='text/xml')

class RegionSelection(TemplateView):

    def render_region_selection_form(self, request, session, redirect_url):
        regions = get_list_or_404(Region)

        # This is the redirect URL to POST the region selected
        redirect_url_POST = reverse('service-development:region', args = [session.id])

        # This is the redirect URL for *AFTER* the region selection process
        pass_on_variables = {'redirect_url' : redirect_url}

        region_options =  Region.objects.values_list('region_name', flat=True)
        language = get_object_or_404(Language, pk=2)
        context = {'regions' : regions,
                    'region_voice_labels': [region_name.voice_label.get_voice_fragment_url(language) for region_name in regions],
                    # 'region_options_redirect_urls': ['vxml/region_redirect/' + str(region_options[n]) for n, _ in enumerate(regions, 0)],
                    'redirect_url' : redirect_url_POST,
                    'pass_on_variables' : pass_on_variables,
                    'language': language
                    }
        return render(request, 'region_selection.xml', context, content_type='text/xml')


    def get(self, request, session_id):
        """
        Asks the user to select one of the supported languages.
        """
        session = get_object_or_404(CallSession, pk = session_id)
        #voice_service = session.service
        #redirect_url = 'vxml/region_redirect/Gao'
        if 'redirect_url' in request.GET:
            redirect_url = request.GET['redirect_url']
        return self.render_region_selection_form(request, session, redirect_url)

    def post(self, request, session_id):
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else: raise ValueError('Incorrect request, redirect_url not set')
        if 'region_id' not in request.POST:
            raise ValueError('Incorrect request, region ID not set')
        session = get_object_or_404(CallSession, pk = session_id)
        #voice_service = session.service
        region = get_object_or_404(Region, pk = request.POST['region_id'])

        session._region = region
        session.save()
        print('done')

        #session.record_step(None, "Region selected, %s" % region.region_name)

        return HttpResponseRedirect(redirect_url)
