__author__ = 'zys'
from django.core.management.base import BaseCommand, CommandError
from designweb.utils import sending_mail_for_new_signup


def testing_call():
    print("crontab is working good !")


class Command(BaseCommand):
    args = '< email_address email_address ...>'
    help = 'please enter email addresses'

    def handle(self, *args, **options):
        for email_address in args:
            try:
                sending_mail_for_new_signup(email_address)
                self.stdout.write('successful send email : "%s"' % email_address)
            except:
                raise CommandError('the email "%s" does not exist' % email_address)
