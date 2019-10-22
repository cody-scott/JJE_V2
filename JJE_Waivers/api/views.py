# from rest_framework import viewsets
#
# from JJE_Waivers.api.serializer import WaiverClaimSerializer
# from JJE_Waivers.models import WaiverClaim
#
# from django.utils import timezone
# from datetime import timedelta
#
#
# class WaiverClaimViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = WaiverClaim.objects.all()
#     serializer_class = WaiverClaimSerializer
#
#
# class ActiveWaiverclaimViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = WaiverClaim.objects.all()
#     serializer_class = WaiverClaimSerializer
#
#     def get_queryset(self):
#         now = timezone.now() - timedelta(days=1)
#         claims = WaiverClaim.objects \
#             .filter(cancelled=False) \
#             .filter(overclaimed=False) \
#             .filter(claim_start__gt=now) \
#             .order_by('claim_start')
#         return claims
