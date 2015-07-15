#-*-coding:utf-8 -*-

def error_ldap_log_message(request, type):
    return 'LDAP connection error type : ' + str(type) + ' par ' + str(request.user)

def error_load_log_message(request):
    return 'user deja connecte essai de charger de la page ' + str(request.META['PATH_INFO']) + ' par ' + str(request.user)

def error_inexistant_user_log_message(request):
    return 'connection avec un user qui n\'existe pas par' + request.POST['username']

def error_login_admin_front_log_message():
    return 'un admin a essaye de se connecter depuis le front comme un boulet'

def error_login_staff_front_log_message():
    return 'un membre dus taff a essaye de se connecter depuis le front comme un boulet'

def error_login_log_message(request):
    return 'authenticate error pour par ' + str(request.POST['username'])

def error_login_unknow_log_message(request):
    return 'le login a pete ion sait pas pourquoi ' + str(request.POST['username'])

def error_login_wrong_password_log_message(request):
    return 'connection avec un mauvais password par ' + str(request.POST['username'])

def error_logout_log_message(request):
    return 'error logout ' + str(request.user)

def error_register_mail_exist(request):
    return 'error register ' + str(request.POST['email']) + 'already exist'

def error_register_user_exist(request):
    return 'error register ' + str(request.POST['username']) + 'already exist'

def info_load_log_message(request):
    return 'chargement de la page ' + str(request.META['PATH_INFO']) + ' par ' + str(request.user)

def info_register_log_message(request):
    return 'creation du compte ' + str(request.user)

def info_login_class_log_message(request):
    return 'connection classique par ' + str(request.user)

def info_login_ldap_log_message(request):
    return 'connection ldap par ' + str(request.user)

def info_logout_log_message(request):
    return 'deconnection par ' + str(request.user)
