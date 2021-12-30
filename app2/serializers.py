
from rest_framework import serializers
from .models import *

import logging

logging.basicConfig(filename='app2.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
# logging.warning('This will get logged to a file')
  
class BooksBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBook
        fields = [
            'id',
            'title',
            'gutenberg_id',
            'download_count',
        ]
    logging.info(f' Serializer called')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # collect author details
        try:
            obj = BooksBookAuthors.objects.filter(book_id=data['id'])
            author_details = []
            for o in obj:
                author_id = o.author_id
                author_obj = BooksAuthor.objects.get(id=author_id)
                author = {}
                author['name']=author_obj.name
                author['birth year']=author_obj.birth_year
                author['death year']=author_obj.death_year
                author_details.append(author)
            data['author']=author_details    
        except Exception as e:
            print("Exception ", e)
            logging.error(f'Exception getting book author : {e}')
            data['author'] = []
        
        # get language details
        try:
            obj = BooksBookLanguages.objects.filter(book_id=data['id'])
            lang_details = []
            for o in obj:
                lang_obj = BooksLanguage.objects.get(id=o.language_id)
                lang_details.append(lang_obj.code)
            data['language'] = lang_details
        except Exception as e:
            logging.error(f'Exception getting language : {e}')
            data['language'] = []
        
        # get subject details
        try:
            obj = BooksBookSubjects.objects.filter(book_id=data['id'])
            sub_details = []
            for o in obj:
                sub_obj = BooksSubject.objects.get(id=o.subject_id)
                sub_details.append(sub_obj.name)
            data['subject'] = sub_details
        except Exception as e:
            logging.error(f'Exception getting book subject : {e}')
            data['subject'] = []

        # get Bookshelves details
        try:
            obj = BooksBookBookshelves.objects.filter(book_id=data['id'])
            bookshelves_details = []
            for o in obj:
                s_obj = BooksBookshelf.objects.get(id=o.bookshelf_id)
                bookshelves_details.append(s_obj.name)
            data['bookshelves'] = bookshelves_details
            data['genre'] = bookshelves_details
        except Exception as e:
            logging.error(f'Exception getting bookshelves : {e}')
            data['bookshelves'] = bookshelves_details
            data['genre'] = bookshelves_details

        # get urls to download
        try:
            obj = BooksFormat.objects.filter(book_id=data['id'])
            download_details = []
            for o in obj:
                dict_download = {}
                dict_download['mime_type']=o.mime_type
                dict_download['url']=o.url
                download_details.append(dict_download)
            data['link_to_download'] = download_details
        except Exception as e:
            logging.error(f'Exception getting urls to download : {e}')
            data['link_to_download'] = []
        
        del data['id']
        del data['gutenberg_id']
        del data['download_count']
        return data
