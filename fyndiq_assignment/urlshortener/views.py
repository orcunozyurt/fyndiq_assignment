from django.shortcuts import render, render_to_response
from models import PairedUrl, WordList
from forms import URLInputForm
from random import randint
import logging
from django.template import RequestContext
from django.http import HttpResponseRedirect

# Create your views here.
def bulk_data(request):
    
    url_form = URLInputForm()
    bulk_data_dict = {}
    bulk_data_dict['url_form'] = url_form
    bulk_data_dict['recent_urls']  = PairedUrl.objects.all().order_by('-cdate')[0:10]
    bulk_data_dict['state'] = 'default'
    
    return bulk_data_dict
    
def index(request):
    context = RequestContext(request)
    bulk = bulk_data(request)

    return render_to_response('urlshortener/index.html', bulk, context)
    
def key_generator(url):
    """
        Method is used for generating a key from the given url.
    """
    word_list_object = None
    url_components = reversed(url.split('/')) #start splitting from end. 
    
    for component in url_components:
        if word_list_object is not None:
            break
        
        words = component.split('-')
        for word in words:
            print word
            try:
                matching_obj = WordList.objects.get(word=word)
                if hasattr(matching_obj, 'pairedurl'):
                    continue
                else:
                    word_list_object = matching_obj
                    break
            
            except WordList.DoesNotExist:
                continue
            
    if word_list_object is None:
        free_words = WordList.objects.filter(is_used=False)
        if(free_words.count() == 0):
            latest_pair = PairedUrl.objects.order_by('cdate')[:1].get()
            print str(latest_pair) + "will be removed.."
            latest_pair.key_generated.is_used=False
            latest_pair.delete()
            
            free_words = WordList.objects.filter(is_used=False)
            
        random = randint(0, len(free_words)-1)
        word_list_object = free_words[random]


    print "the alias is " + str(word_list_object.word)
        
    return word_list_object
    
    
def submit(request):
    """
    View for submitting the URLs.
    :param request:
    :return:
    """
    context = RequestContext(request)
    url = None
    url_form = None
   
    if request.method == 'GET':
        url_form = URLInputForm(request.GET)
    elif request.method == 'POST':
        url_form = URLInputForm(request.POST)
    
    values = bulk_data(request)
    values['state'] = "submitted"
    if url_form and url_form.is_valid():
        print url_form.cleaned_data
        url = url_form.cleaned_data['url_input']
        print "URL:"+url
        link = None
        wobj = None
        try:
            obj = PairedUrl.objects.get(url=url)
            wobj = obj.key_generated
        except PairedUrl.DoesNotExist:
            logging.log(logging.INFO, "URL %s doesn't already exist", url)
            pass

        if wobj is None:
            wobj = key_generator(url)
            logging.log(logging.INFO, "Generated link %s", wobj.word)
            obj = PairedUrl(url=url, key_generated=wobj,)
            obj.save()
            logging.log(logging.INFO, "Saving into database.")

        values['status'] = True
        values['alias'] = wobj.word
        values['fullurl'] = wobj.pairedurl.url
        return render_to_response('urlshortener/index.html', values, context)

    values['status'] = False
    return render_to_response('urlshortener/index.html', values, context)
    
    
def redirect(request):
    alias = request.path
    alias = alias.replace('/', '')
    try:
        obj = WordList.objects.get(word=alias)
        if hasattr(obj, 'pairedurl'):
            pairedurl = obj.pairedurl
            return HttpResponseRedirect(pairedurl.url)
        else:
            values = bulk_data(request)
            values['messages'] = ["Alias '%s' is Unused" % alias,]
            return render_to_response('urlshortener/index.html', values, RequestContext(request))
    except WordList.DoesNotExist:
        logging.log(logging.ERROR, "Can't redirect %s", alias)
        values = default_values(request)
        values['status'] = False
        values ['state'] = 'redirecterror'
        values['messages'] = ["No Alias '%s' found" % alias,]
        return render_to_response('urlshortener/index.html', values, RequestContext(request))
