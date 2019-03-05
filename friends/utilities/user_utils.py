from django.contrib.auth import get_user_model


class UserUtils:
    """
    Utilities for users.
    """

    @staticmethod
    def get_brian_bot():
        """
        Returns the Brian Bot user. Raises an exception if it does not exist.
        :return: The Brian Bot user.
        """
        return get_user_model().objects.get(is_brian_bot=True)

    @staticmethod
    def exclude_brian_bot(queryset=None):
        """
        Given a queryset for users, excludes Brian Bot from it. If none is given, returns a new such queryset.
        :param queryset: A queryset for users. (optional)
        :return: The given queryset with Brian Bot excluded, or a new such queryset if none is given.
        """
        if not queryset:
            queryset = get_user_model().objects
        return queryset.exclude(is_brian_bot=True)
