import os
import shutil

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import default_storage

from documents.conf.settings import STAGING_DIRECTORY    
from documents.conf.settings import UUID_FUNCTION    
from models import Document, get_filename_from_uuid


def get_all_files():
    return sorted([os.path.normcase(f) for f in os.listdir(STAGING_DIRECTORY)])


class StagingFile(object):
    @classmethod
    def get_all(cls):
        staging_files = []
        for id, filename in enumerate(get_all_files()):
            staging_files.append(StagingFile(
                filepath=os.path.join(STAGING_DIRECTORY, filename),
                id=id))
        
        return staging_files

    @classmethod
    def get(cls, id):
        files = get_all_files()
        if id <= len(files):
            return StagingFile(
                filepath=os.path.join(STAGING_DIRECTORY, files[id]),
                id=id)
        raise ObjectDoesNotExist

    def __init__(self, filepath, id):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self._id = id
        
    def __unicode__(self):
        return self.filename

    def __repr__(self):
        return self.__unicode__()

    def __getattr__(self, name):
        if name == 'id':
            return self._id
        else:
            raise AttributeError, name

    def upload(self, document_type):
        document = Document(document_type=document_type)
        document.save(save=False)
        print 'UUID', document.uuid
        tmp_filepath = os.path.join(settings.MEDIA_ROOT, UUID_FUNCTION())
        #shutil.copy(self.filepath, tmp_filepath)
        #document = Document(document_type=document_type,
        #    file=tmp_filepath)
        #document.save()
        #final_filepath = get_filename_from_uuid(document, filename=self.filename)
        #document.save()
        #print final_filepath

        