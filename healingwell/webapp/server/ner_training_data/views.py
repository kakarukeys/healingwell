from healingwell.webapp.server.api import api, RestrictedAccessResource
from healingwell.crawler.models import GERD
from healingwell.NER.models import NERTrainingData


class GERDResource(RestrictedAccessResource):
	fields = ("post_content",)

class NERTrainingDataResource(RestrictedAccessResource):
	include_resources = {"gerd": GERDResource}

api.register(GERD, GERDResource)
api.register(NERTrainingData, NERTrainingDataResource)

api.setup()
