import mandrill

def build_message(sender, receiver, subject, message, options):
    message = {'from_email': sender,
                'merge': True,
                'to': [{'email': receiver, 'name': ''}],
                'subject':subject,
                'text':message,
                }
    return message

def send_mail(subject, message, sender, receivers, 
                fail_silently=True, options = {}):
    for email in receivers:
        try:
            mandrill_client = mandrill.Mandrill('kXCZlI-9tCRJFfQXGRixzA')
            mail = build_message(sender, email, subject, message, options)
            result = mandrill_client.messages.send(message=mail, async=False, ip_pool='Main Pool', send_at=None)
        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.InvalidKeyError'> - Invalid API key    
            raise