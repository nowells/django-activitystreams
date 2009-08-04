"""
The PickleField has been adapted from http://www.djangosnippets.org/snippets/513/
"""

import codecs

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models
from django.utils.encoding import smart_unicode

class PickledObject(str):
    """A subclass of string so it can be told whether a string is
    a pickled object or not (if the object is an instance of this class
    then it must [well, should] be a pickled one)."""
    pass

class PickleField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def value_to_string(self, obj):
        return smart_unicode(self.get_db_prep_save(self._get_val_from_obj(obj)))

    def to_python(self, value):
        if value:
            if isinstance(value, unicode):
                enc = codecs.getencoder('utf8')
                return pickle.loads(enc(value)[0])
            elif isinstance(value, str):
                return pickle.loads(value)
        return value

    def get_db_prep_save(self, value):
        if value is not None and not isinstance(value, PickledObject):
            value = PickledObject(pickle.dumps(value))
        return value

    def get_internal_type(self):
        return 'TextField'

    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            value = self.get_db_prep_save(value)
            return super(PickleField, self).get_db_prep_lookup(lookup_type, value)
        elif lookup_type == 'in':
            value = [self.get_db_prep_save(v) for v in value]
            return super(PickleField, self).get_db_prep_lookup(lookup_type, value)
        else:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)
