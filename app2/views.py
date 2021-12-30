from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
from .serializers import *

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import app2
import math

from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

import logging

logging.basicConfig(filename='app2.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)

@csrf_exempt
def book_list(request):
    """
    API which returns list of books with their details 
    """
    try:
        if request.method == "GET":
            page_no = request.GET.get('page',1) # get page_no from UI
            gutenberg_id = request.GET.get('gutenberg_id',None)
            language = request.GET.get('language',None)
            mime_type = request.GET.get('mime_type',None)
            topic = request.GET.get('topic',None)
            author = request.GET.get('author',None)
            title = request.GET.get('title',None)

            # print("Input data : ", request.GET)
            logging.info(f'Input data for book_list API : {request.GET}')

            # validations for page_no
            if not type(int(page_no))== int:
                return JsonResponse({"message": "Enter Integer Page Number"},status=400)
            if int(page_no)<=0:
                return JsonResponse({"message": "Incorrect Page Number"},status=400)
            # books=[]
            if gutenberg_id or language or mime_type or topic or author or title:
                books = get_filtered_data(gutenberg_id,language,mime_type,topic,author,title)
            else:
                books = BooksBook.objects.filter(id__lte=300)
            
            serializer = BooksBookSerializer(books, many=True)
            logging.info(f'pagination')
            # pagination
            if serializer.data:
                max_count = math.ceil(len(serializer.data)/25)
                if int(page_no) > max_count:
                    return JsonResponse({"message": "page_no_not_correct"},status=400)
                # Pagination
                paginator = Paginator(serializer.data, 25)
                pages_no = request.GET.get('page')
                page = paginator.page(pages_no)

                return JsonResponse({"books":page.object_list,"max_page_count":max_count,"max_record_count":len(serializer.data)},status=200)
            else:
                return JsonResponse({"books":"No book found with given filter"},status=200)
            # return JsonResponse(serializer.data, safe=False)
        logging.error(f'Invalid requets type ')
        return JsonResponse({"message":"Invalid request"},status=500)
    except Exception as e:
        logging.error(f'Exception book_list API : {e}')
        return JsonResponse({"message":"Something went wrong, please try again later"},status=403)

    # return HttpResponse("hello")


#### functions to get primary keys based on filter criteria ####
def get_pks_from_lang(language):
    try:
        language = language.split(",")
        lang_id = [ i.id for i in BooksLanguage.objects.filter(code__in=language)]
        pks_from_lang = [i.book_id for i in BooksBookLanguages.objects.filter(language_id__in=lang_id)]
        logging.info(f'get_pks_from_lang - pks_from_lang : {len(pks_from_lang)}')
        return pks_from_lang
    except Exception as e:
        return []

def get_pks_from_author(author):
    try:
        auth_id = [ i.id for i in  BooksAuthor.objects.filter(name__icontains=author)]
        pks_from_author = [i.book_id for i in BooksBookAuthors.objects.filter(author_id__in=auth_id)]
        # print("get_pks_from_author - pks_from_author : ",len(pks_from_author))
        logging.info(f'get_pks_from_author - pks_from_author : {len(pks_from_author)}')
        return pks_from_author
    except Exception as e:
        return []

def get_pks_from_mimetype(mime_type):
    try:
        pks_from_mimetype = [i.book_id for i in BooksFormat.objects.filter(mime_type=mime_type)]
        # print("get_pks_from_mimetype - pks_from_mimetype : ",len(pks_from_mimetype))
        logging.info(f'get_pks_from_mimetype - pks_from_mimetype : {len(pks_from_mimetype)}')
        return pks_from_mimetype

    except Exception as e:
        return []

def get_pks_from_topic(topic):
    try:
        shelf_id = [ i.id for i in BooksBookshelf.objects.filter(name__icontains=topic)]
        pks_from_shelf = [i.book_id for i in BooksBookBookshelves.objects.filter(bookshelf_id__in=shelf_id)]
        sub_id = [ i.id for i in BooksSubject.objects.filter(name__icontains=topic)]
        pks_from_sub = [i.book_id for i in BooksBookSubjects.objects.filter(subject_id__in=sub_id)]
        pks_from_topic = list(set(pks_from_shelf) | set(pks_from_sub))
        logging.info(f"get_pks_from_topic - pks_from_shelf - pks_from_sub - pks_from_topic : {len(pks_from_shelf),len(pks_from_sub),len(pks_from_topic)}")
        return pks_from_topic

    except Exception as e:
        return []


#### get filtered data ###

def get_filtered_data(gutenberg_id,language,mime_type,topic,author,title):
    if gutenberg_id and title:
        main_pks = get_main_pks(mime_type, language, author, topic)
        if not main_pks:
            logging.info(f"main pks is empty for - gutenberg_id and title ")
            return BooksBook.objects.filter(gutenberg_id=gutenberg_id,title__icontains=title).order_by('-download_count')

        logging.info(f"main_pks - length - {len(main_pks)}")
        return BooksBook.objects.filter(id__in = main_pks,gutenberg_id=gutenberg_id, title__icontains=title).order_by('-download_count')
    
    elif gutenberg_id and not title:
        main_pks = get_main_pks(mime_type, language, author, topic)
        if not main_pks:
            logging.info(f"main pks is empty for - gutenberg_id and not title ")
            return BooksBook.objects.filter(gutenberg_id=gutenberg_id).order_by('-download_count')
        logging.info(f"main_pks  - length - {len(main_pks)}")
        return BooksBook.objects.filter(id__in = main_pks, gutenberg_id=gutenberg_id).order_by('-download_count')
    
    elif title and not gutenberg_id :
        main_pks = get_main_pks(mime_type, language, author, topic)        
        if not main_pks:
            logging.info(f"main pks is empty for - not gutenberg_id and title ")
            return BooksBook.objects.filter(title__icontains=title).order_by('-download_count')
        logging.info(f"main_pks  - length - {len(main_pks)}")
        return BooksBook.objects.filter(id__in = main_pks, title__icontains=title).order_by('-download_count')
        
    else:
        main_pks = get_main_pks(mime_type, language, author, topic)
        if not main_pks:
            logging.info(f"main pks is empty for - else ")
            return BooksBook.objects.filter().order_by('-download_count')
        logging.info(f"main_pks  - length - {len(main_pks)}")
        return BooksBook.objects.filter(id__in = main_pks).order_by('-download_count')


def get_main_pks(mime_type, language, author, topic):
    """
    This function collects bbook id i.e. pks from respective tables
    """
    try:
        pks_from_lang = []
        pks_from_author = []
        pks_from_mimetype = []
        pks_from_topic = []
        main_pks = []

        if mime_type:
            logging.info(f'filtering on mime_type------------1')
            pks_from_mimetype = get_pks_from_mimetype(mime_type)
            if pks_from_mimetype:
                main_pks = list(set(pks_from_mimetype))

                if language:
                    logging.info(f'filtering on language------------2')
                    pks_from_lang = get_pks_from_lang(language)
                    if pks_from_lang:
                        # main_pks = list(set(pks_from_lang) & set(pks_from_mimetype))
                        main_pks = list(set(main_pks) & set(pks_from_lang))

                        if author:
                            logging.info(f'filtering on author------------3')
                            pks_from_author = get_pks_from_author(author)
                            if pks_from_author:

                                # main_pks = list(set(pks_from_lang) & set(pks_from_author) & set(pks_from_mimetype) )
                                main_pks = list(set(main_pks) & set(pks_from_author))

                                if topic:
                                    logging.info(f'filtering on topic---4')
                                    pks_from_topic = get_pks_from_topic(topic)
                                    if pks_from_topic:
                                        main_pks = list(set(main_pks) & set(pks_from_topic))
                                        # return main_pks
                                        # main_pks = list(set(pks_from_lang) & set(pks_from_author) & set(pks_from_mimetype) & set(pks_from_topic))
                                    logging.info(f'no result for filtering on topic---4')
                                    return main_pks            
                                return main_pks
                            logging.info(f'no result for filtering on author---3')   
                            return main_pks    
                        return main_pks
                    logging.info(f'no result for filtering on language---2')   
                    return main_pks
                return main_pks
            logging.info(f'no result for filtering on mime_type---1')  
            return main_pks
        return main_pks
    except Exception as e:
        logging.error(f'Exception get_main_pks(mime_type, language, author, topic) : {e}')
        return []
