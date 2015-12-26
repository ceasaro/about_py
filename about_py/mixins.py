from django.contrib.auth.mixins import AccessMixin


class IsStaffOrSuperUserMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or request.user.is_superuser:
            return self.handle_no_permission()
        return super(IsStaffOrSuperUserMixin, self).dispatch(request, *args, **kwargs)
