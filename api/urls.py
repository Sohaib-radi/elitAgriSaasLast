from django.urls import path, include
from core.views.auth import CreateUserView, MeView, MyFarmsView, UpdateCurrentUserView,AdminUpdateTeamMemberView
from core.views.role import RoleListView
from core.views.team import TeamMemberView
from core.views.team import TeamMemberInviteView
from core.views.team import TeamMemberDetailView
from core.views.auth import CustomLoginView
from core.views.auth import SignupView
from core.views.auth import SwitchFarmView
from core.views.audit import UserLogListView
from core.views.team import InviteUserView
from core.views.auth import AcceptInviteView
from core.views.permissions import MyPermissionsView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # Login
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # Refresh
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),         # (Verify Token)
]

urlpatterns += [
    path('auth/me/', MeView.as_view(), name='auth_me'),
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('team-members/', TeamMemberView.as_view(), name='team-member-list-create'),
    path('team-members/invite/', TeamMemberInviteView.as_view(), name='team-member-invite'),
    path('team-members/<int:pk>/', TeamMemberDetailView.as_view(), name='team-member-detail'),
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path("auth/switch-farm/", SwitchFarmView.as_view(), name="switch-farm"),
    path('audit-logs/', UserLogListView.as_view(), name='audit-logs'),
    path('team/invite/', InviteUserView.as_view(), name='invite-user'),
    path('auth/accept-invite/', AcceptInviteView.as_view(), name='accept-invite'),
    path("auth/my-permissions/", MyPermissionsView.as_view(), name="my_permissions"),
    path("auth/my-farms/", MyFarmsView.as_view(), name="my-farms"),
    path("settings/farm/", include("farm_settings.urls")),
    path('auth/user/create/', CreateUserView.as_view(), name='user-create'),
    path('auth/user/update/', UpdateCurrentUserView.as_view(), name='user-update'),
    path('team-member/<int:team_member_id>/edit/', AdminUpdateTeamMemberView.as_view(), name='team-member-update')
]

urlpatterns +=[
    path("settings/farm/", include("farm_settings.urls")),
    path("animal/", include("animal.urls")),
    path("land/", include("land.urls")),
    path('products/', include('product_catalogue.urls')),
    path("warehouse/", include("warehouse.urls")),
    path("crop/", include("crop.urls")),
    path("finance/", include("finance.urls")),
    path("core/", include("core.urls")),
    path("projects/",include("assets_projects.urls")),
    path('dashboard/', include('dashboard.urls')),

]