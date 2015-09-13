from django.shortcuts import render, render_to_response
from models import PairedUrl, WordList
from forms import URLInputForm
from random import randint
import logging
from django.template import RequestContext
from django.http import HttpResponseRedirect

# Create your views here.
def bulk_data(request):
    """
        Method was created to serve data from db as easy as possible
        url_form : form to get url input
        recent_urls : last 10 conversions to show on main page(not a part of assignment-optional)
        state : state variable for cases of form submitted - on error etc.
    """
    url_form = URLInputForm()
    bulk_data_dict = {}
    bulk_data_dict['url_form'] = url_form
    bulk_data_dict['recent_urls']  = PairedUrl.objects.all().order_by('-cdate')[0:10]
    bulk_data_dict['state'] = 'default'
    
    return bulk_data_dict
    
def index(request):
    """
        View for index page..
        Sending the bulk_data() to index.html 
    """
    context = RequestContext(request)
    bulk = bulk_data(request)

    return render_to_response('urlshortener/index.html', bulk, context)
    
def key_generator(url):
    """
        example url:http://techcrunch.com/2012/12/28/pinterest-lawsuit/ 
        Method is used for generating a key from the given url.
        Going to split the url by "/" and extract components
        Then split by "-" to get the keys to be used in shortened url
    """
    word_list_object = None
    url_components = reversed(url.split('/')) #start splitting from end.(url_components:pinterest-lawsuit) 
    
    for component in url_components:  
        if word_list_object is not None:
            break
        
        words = component.split('-') #(words:[pinterest,lawsuit]) 
        for word in words:
            print word # Seeing the word on console calms me down but it is bad practice..
            # Now it is time to try to get a matching alias from wordlist.
            try:
                matching_obj = WordList.objects.get(word=word)
                if hasattr(matching_obj, 'pairedurl'):
                    continue
                else:
                    word_list_object = matching_obj
                    break
            
            except WordList.DoesNotExist:
                continue
            
    if word_list_object is None:   # If Cant find any matching word for some reason..
        free_words = WordList.objects.filter(is_used=False) # get the words that are still free..
        if(free_words.count() == 0): # If no free words we should get the oldest pair and delete
            latest_pair = PairedUrl.objects.order_by('cdate')[:1].get()
            print str(latest_pair) + "will be removed.."
            latest_pair.key_generated.is_used=False #and free the word from the word list.
            latest_pair.delete()
            
            free_words = WordList.objects.filter(is_used=False)# search for free word again..
            
        random = randint(0, len(free_words)-1) # pick a random word from free words.
        word_list_object = free_words[random]


    print "the alias is " + str(word_list_object.word) # seeing the process on console..
        
    return word_list_object
    
    
def submit(request):
    """
    View for submitting the URLs. It is both fine to POST or GET 
    :param request:
    :return:
    """
    context = RequestContext(request)
    url = None
    url_form = None
    
    # Handle both POST and GET Requests.
    if request.method == 'GET':
        url_form = URLInputForm(request.GET)
    elif request.method == 'POST':
        url_form = URLInputForm(request.POST)
    
    values = bulk_data(request) # bulk data method we created at the begining.
    values['state'] = "submitted" # Form is submitted , so change the state.
    if url_form and url_form.is_valid(): # URL validation..
        
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
    """
     Match the alias and redirect to original URL.
     
    """
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
