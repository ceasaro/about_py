from django.contrib.auth.views import redirect_to_login


class IsStaffOrSuperUserMixin(object):
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or request.user.is_superuser:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(),
                                     self.get_redirect_field_name())
        return super(IsStaffOrSuperUserMixin, self).dispatch(request, *args, **kwargs)
