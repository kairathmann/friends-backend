from django.contrib.auth import get_user_model


class UserUtils:
    """
    Utilities for users.
    """

    @staticmethod
    def get_luminos_bot():
        """
        Returns the Luminos Bot user. Raises an exception if it does not exist.
        :return: The Luminos Bot user.
        """
        return get_user_model().objects.get(is_luminos_bot=True)

    @staticmethod
    def exclude_luminos_bot(queryset=None):
        """
        Given a queryset for users, excludes Luminos Bot from it. If none is given, returns a new such queryset.
        :param queryset: A queryset for users. (optional)
        :return: The given queryset with Luminos Bot excluded, or a new such queryset if none is given.
        """
        if not queryset:
            queryset = get_user_model().objects
        return queryset.exclude(is_luminos_bot=True)
