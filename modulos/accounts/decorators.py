from django.contrib import messages
from django.shortcuts import redirect

def allowed_users(perm, redirect_url=None):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if isinstance(perm, str):
				perms = (perm,)
			else:
				perms = perm
			# First check if the user has the permission (even anon users)
			if request.user.has_perms(perms):
				return view_func(request, *args, **kwargs)
			else:
				messages.error(request, "¡Acceso Restringido, no tiene los permisos requeridos!")
				if redirect_url is None:
					return redirect('/')
				else:
					return redirect(redirect_url)
		return wrapper_func
	return decorator