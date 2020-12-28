from rest_framework.response import Response
from rest_framework.views import APIView

from rdflib import Graph


class SyncMetadataRDF(APIView):
    """
    Sync's metadata with triple store 
    """

    def post(self, request, col_id, format=None):
        try:
            res_uri = settings.ARVADOS_COL_BASE_URI + col_id + "/metadata.rdf"
            g = Graph()
            g.parse(res_uri)
            insert(g)
            return Response()
        except Exception as e:
            logger.exception("message")

