from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.http import HttpResponseNotFound
from ..models import *

class LendRentSelection(TemplateView):
    def render_selection(self, request, session):
        # regions = get_list_or_404(Region)

        # This is the redirect URL to POST the region selected
        redirect_url_POST = reverse( 'service-development:lendrent', kwargs= {'session_id':session.id})

        # This is the redirect URL for *AFTER* the region selection process
        vse_element = vse_element = get_object_or_404(Vse_Own_Added, name='lendrent')
        pass_on_variables = {'redirect_url' : vse_element.redirect.get_absolute_url(session=session)}

        # region_options =  Region.objects.values_list('region_name', flat=True)
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
        return self.render_selection(request, session)

    def post(self, request, session_id):
        try:
            if 'region_id' not in request.POST:
                raise ValueError('Incorrect request, region ID not set')
        except: 
            return HttpResponseNotFound('No change made')

        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service
        region = get_object_or_404(Region, pk = request.POST['region_id'])
        #print(type(request.POST['region_id']))
        lend_bool == True if request.POST['lending'] == 1 else False
        session._lending = lend_bool
        session.save()
        # print('done')

        
        # session.record_step(None, "Region selected, %s" % region.region_name)
        vse_element = get_object_or_404(Vse_Own_Added, name='region')
        # print(vse_element.redirect.get_absolute_url(session=session))
        return HttpResponseRedirect(vse_element.redirect.get_absolute_url(session=session))