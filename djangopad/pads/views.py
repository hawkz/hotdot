from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail

from pads.models import Pad, TextArea
from pads.forms import PadForm, TextAreaForm
from pads.utility import create_pad_guid

from datetime import datetime
from hashlib import md5


#dont allow questions that are already url names:
DISALLOWED_QUESTIONS = ["", "new", "vote"]

def index(request):
    '''user_pads, recent_pads sent to 'pads/index.html'

    '''

    users_pads = Pad.objects.filter( owner=request.user )
    recent_pads = Pad.objects.all()

    return object_list( request,
        queryset = Pad.objects.all(),
        paginate_by = 50,
        template_name = 'pads/index.html',
        extra_context = locals(),
    )

@login_required
def detail(request, owner, slug):
    '''The Pad object_detail

    '''
    #TODO: check if user is logged in, then enable chat, etc.

    slug_guid = create_pad_guid(slug)

    try:
        pad = Pad.objects.get(guid=slug_guid)

    except Pad.DoesNotExist:
        raise Http404

    textareas = TextArea.objects.filter(pad=pad)

    if not textareas:
        textarea_a = TextArea( pad=pad, content="", editor=request.user )
        textarea_a.save()

    else:
        textarea_a = textareas[0]

    args = {"textarea_a":textarea_a, "user":request.user,
            'textareas': textareas,
            "STOMP_PORT":settings.STOMP_PORT, "CHANNEL_NAME": slug_guid,
            "HOST":settings.INTERFACE, "SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME}

    return object_detail( request,
            queryset = Pad.objects.all(),
            object_id = pad.id,
            template_object_name = 'pad',
            template_name = 'pads/pad.html',
            extra_context = args,
    )


@login_required
def new(request):
    """
    Create a new Pad, with 1 initial "TextArea" for
    a given choice.

    """
    if request.method == 'POST':
        pad_form = PadForm(request.POST)

        if pad_form.is_valid():
            pad_inst = pad_form.save(commit=False)
            title = pad_form.cleaned_data["title"]

            # TODO is there a reason that this is not factored out to the
            # forms.py?

            pad_inst.owner = request.user
            pad_inst.last_modified = datetime.now()
            pad_inst.guid = create_pad_guid(title)
            pad_inst.save()

            textarea_inst = TextArea(pad=pad_inst, editor=request.user )
            textarea_inst.save()
            return HttpResponseRedirect('/') # Redirect after POST

    else:
        pad_form = PadForm()

    args = {"pad_form":pad_form, "user":request.user}

    return create_object( request,
            form_class = PadForm,
            template_name = 'pads/new.html',
            extra_context = args,
            #login_required = True,
    )

