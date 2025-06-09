from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadCreateOnly(BasePermission):
    """
    Custom permission:
    - Anyone can create or list their own orders.
    - Only the owner can retrieve, update, or delete.
    """

    def has_permission(self, request, view):
        # Anyone authenticated can access list/create
        if view.action in ['list', 'create']:
            return request.user and request.user.is_authenticated
        # Let object-level permission handle the rest
        return True

    def has_object_permission(self, request, view, obj):
        # Only allow object access if the user owns it
        return obj.user == request.user
