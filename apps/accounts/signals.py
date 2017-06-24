import logging
from datetime import datetime
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_login_failed

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_when_user_was_logged(sender, **kwargs):
    user = kwargs['user']
    logger.info('User: {} was logged in at {}'.format(user.email, datetime.now()))


@receiver(user_login_failed)
def log_when_user_login_failed(sender, **kwargs):
    logger.warning('Login Failed! Username: {}; Time: {}'.format(kwargs['credentials']['username'], datetime.now()))
