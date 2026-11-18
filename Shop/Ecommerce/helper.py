from django.core.mail import send_mail

def custom_mail(title:str, message:str, reply_to='reply@somethinggmail.com', receptients=[]):
    try:
        send_mail(
            f'Bussiness : {title}',
            message,
            reply_to,            # uses DEFAULT_FROM_EMAIL
            receptients,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print("Error : ",e)
        return False