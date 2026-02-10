from rest_framework.routers import DefaultRouter
from .viewsets import UserFormViewSet

router = DefaultRouter()
router.register("user-forms", UserFormViewSet, basename="user-forms")

urlpatterns = router.urls
