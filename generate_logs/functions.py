#-*-coding:utf-8 -*-

def info_load_log_message(request):
    return 'chargement de la page ' + str(request.META['PATH_INFO']) + ' par ' + str(request.user)

def info_register_log_message(request):
    return 'vreation du compte ' + str(request.user)

def info_login_class_log_message(request):
    return 'connection classique par ' + str(request.user)

def info_login_ldap_log_message(request):
    return 'connection ldap par ' + str(request.user)

def info_logout_log_message(request):
    return 'deconnection par ' + str(request.user)
