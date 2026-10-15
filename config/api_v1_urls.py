"""Version 1 API route table.

ViewSets are registered on this router as each module is implemented.
"""

from rest_framework.routers import DefaultRouter

app_name = "api_v1"

router = DefaultRouter()

urlpatterns = [*router.urls]
