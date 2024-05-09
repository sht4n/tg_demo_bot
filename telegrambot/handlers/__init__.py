from .admin import router as admin_router
from .common import router as common_router
from .common_defending import router as last_frontier_router
from .feeding import router as feed_router
from .questioning import router as questionnaire_router


ROUTERS = (
    admin_router,
    common_router,
    questionnaire_router,
    feed_router,
    last_frontier_router,             
)
