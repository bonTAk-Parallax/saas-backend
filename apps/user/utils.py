
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.models import User

def get_jwt_response(user: User) -> dict:
    """
    Reusable utility to generate JWT tokens for a user.
    Used in Login, Registration, and any "auto-login-after-signup" flows.
    """
    refresh = RefreshToken.for_user(user)
    
    refresh.access_token['user_id'] = user.id
    refresh.access_token['username'] = user.username
    refresh.access_token['org_id'] = user.profile.organization.id
    refresh.access_token['is_admin'] = user.profile.role == 'ADMIN'  
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'org_id': user.profile.organization.id,
            'org_name': user.profile.organization.name,
        }
    }

