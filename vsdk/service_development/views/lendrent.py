from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.http import HttpResponseNotFound
from ..models import *
import sys

class LendRentSelection(TemplateView):
    def render_selection(self, request, session):
        # regions = get_list_or_404(Region)

        # This is the redirect URL to POST the region selected
        redirect_url_POST = reverse( 'service-development:lendrent', kwargs= {'session_id':session.id})

        # This is the redirect URL for *AFTER* the region selection process
        vse_element = vse_element = get_object_or_404(Vse_Own_Added, name='lendrent')
        pass_on_variables = {'redirect_url' : vse_element.redirect.get_absolute_url(session=session)}

        # region_options =  Region.objects.values_list('region_name', flat=True)
        language = session.language
        context = {'returning_options' : [0, 1],
                   'question_url': get_object_or_404(VoiceLabel, name='lend_or_rent').get_voice_fragment_url(language),
                    'choice_labels': [get_object_or_404(VoiceLabel, name='rent_a_product').get_voice_fragment_url(language),
                                            get_object_or_404(VoiceLabel, name='lend_a_product').get_voice_fragment_url(language)],
                    # 'region_options_redirect_urls': ['vxml/region_redirect/' + str(region_options[n]) for n, _ in enumerate(regions, 0)],
                    'redirect_url' : redirect_url_POST,
                    'pass_on_variables' : pass_on_variables,
                    'language': language
                    }
        return render(request, 'lend_rent.xml', context, content_type='text/xml')


    def get(self, request, session_id):
        """
        Asks the user to select one of the supported languages.
        """
        session = get_object_or_404(CallSession, pk = session_id)
        return self.render_selection(request, session)

    def post(self, request, session_id):
        try:
            if 'lending' not in request.POST:
                raise ValueError('Incorrect request, region ID not set')
        except: 
            return HttpResponseNotFound('No choice made')

        session = get_object_or_404(CallSession, pk = session_id)

        if request.POST['lending'] == '1' or \
            request.POST['lending'] == 1:
            lend_bool = True
        else:
            lend_bool = False
        # lend_bool = True if request.POST['lending'] == 1 else False
        # sys.stdout.write(request.POST['lending'])
        # sys.stdout.write(str(type(request.POST['lending'])))
        # sys.stdout.write(str(request.POST))
        session._lending = lend_bool
        session.save()
        # print('done')

        
        # session.record_step(None, "Region selected, %s" % region.region_name)
        vse_element = get_object_or_404(Vse_Own_Added, name='lendrent')
        # print(vse_element.redirect.get_absolute_url(session=session))
        return HttpResponseRedirect(vse_element.redirect.get_absolute_url(session=session))