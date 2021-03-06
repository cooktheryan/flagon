from django.db import models

from flagon import errors
from flagon.backends import Backend
from flagon.backends.db_django.models import FlagonParams, FlagonFeature


class DjangoORMBackend(Backend):

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        try:
            FlagonFeature.objects.get(name=name)
            return True
        except FlagonFeature.DoesNotExist:
            return False

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        try:
            feature = FlagonFeature.objects.get(name=name)
            return feature.active
        except FlagonFeature.DoesNotExist:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

    def _turn(self, name, value):
        """
        Turns a feature on or off

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        try:
            feature = FlagonFeature.objects.get(name=name)
            feature.active = bool(value)
            feature.save()
        except FlagonFeature.DoesNotExist:
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

    turn_on = lambda s, name: s._turn(name, True)
    turn_off = lambda s, name: s._turn(name, False)
