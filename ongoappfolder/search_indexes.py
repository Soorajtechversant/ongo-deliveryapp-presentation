import datetime
from haystack import indexes
from requests import request
from ongoappfolder.models import MerchantDetails , HotelName

class HotelNameIndex(indexes.SearchIndex, indexes.Indexable):
   
    text = indexes.CharField(document = True , use_template = True)
    content_auto = indexes.EdgeNgramField(model_attr='hotel_name')

    def get_model(self):
        return MerchantDetails

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class FoodNameIndex(indexes.SearchIndex, indexes.Indexable):
   
    text = indexes.CharField(document = True , use_template = True)
    content_auto = indexes.EdgeNgramField(model_attr='food')

    def get_model(self):
        return HotelName

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
