from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy


class PermissionMixin(object):

    permission_required = None
    permission_denied_message = None
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No dispone de los permisos necesarios')
        return redirect(self.url_redirect or reverse_lazy('index'))