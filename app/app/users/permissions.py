from rest_framework.permissions import BasePermission


class canCreateTeam(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return request.user.is_authenticated and (request.user.team == None)


class canInvite(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_invite


class hasTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.team != None)
