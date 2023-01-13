import datetime
from haystack import indexes
from requests import request
from ongoappfolder.models import MerchantDetails

class HotelNameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True , use_template = True)
   
    # pub_date = indexes.DateTimeField(model_attr='pub_date')
    # if request.method == 'GET':
    #     content_auto = indexes.EdgeNgramField(model_attr='hotelname')
    # else:
    #     content_auto = indexes.EdgeNgramField(model_attr='food')
    content_auto = indexes.EdgeNgramField(model_attr='hotel_name')

    def get_model(self):
        return MerchantDetails

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
