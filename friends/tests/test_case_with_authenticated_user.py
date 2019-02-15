from .test_case_with_data import TestCaseWithData


class TestCaseWithAuthenticatedUser(TestCaseWithData):

    def setUp(self):
        super(TestCaseWithAuthenticatedUser, self).setUp()
        self.addAuthenticatedUser()
