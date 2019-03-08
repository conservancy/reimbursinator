from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from backend.models import Report
from users.models import CustomUser
from unittest.mock import Mock, patch
from datetime import date
from backend.views import *

class ReportTests(TestCase):

    def create_test_user(self, email, first, last, password):
        """
        Create a test user and return it.
        """
        user = CustomUser.objects.create_user(username=email, email=email, first_name=first, last_name=last, password=password)
        return user

    def mock_report():
        """
        Generates a mock object with the attributes of a report.
        """
        r = Mock()
        r.report_pk = 1
        r.title = 'Report Title'
        r.date_created = '2019-03-01'
        r.date_submitted = '2019-03-01'
        r.submitted = False
        r.reference_number = '12345'
        return r

    def setUp(self):
        """
        Create a test user and save it in the database.
        """
        self.test_user_1 = self.create_test_user('one@one.com', 'One', 'Mr. One', '1password')
        self.test_user_1.save()
 
    def test_create_report_logged_in(self):
        """
        Test when an authenticated user tries to submit a report.
        """
        factory = APIRequestFactory()
        request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(request, user=user)
        response = create_report(request)
        self.assertEqual(response.status_code, 200)
        report = Report.objects.get(user_id=user)
        self.assertEqual(report.title, 'Test Report')

    def test_create_report_logged_out(self):
        """
        Test when an unauthenticated user tries to create a report.
        """
        factory = APIRequestFactory()
        request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        response = create_report(request)
        self.assertEqual(response.status_code, 401)

    @patch('backend.models.Report.objects.filter', Mock(return_value=[mock_report()]))
    @patch('backend.views.get_sections', Mock(return_value={}))
    def test_get_report(self):
        result = get_report(1)
        self.assertEqual(
            result,
            {
                'date_created':'2019-03-01',
                'reference_number':'12345',
                'report_pk':1,
                'title':'Report Title',
                'date_submitted':'2019-03-01',
                'submitted':False
            }
        )

    def test_report_submit_for_review_logged_out(self):
        """
        Test for when an unauthenticated user tries to submit a report for review.
        """
        factory = APIRequestFactory()
        request = factory.put('/api/v1/report/1')
        response = create_report(request)
        self.assertEqual(response.status_code, 401)

    def test_report_submit_for_review_logged_in_not_finalized(self):
        """
        Test for when an authenticated user tries to submit for review a report
        that has not been finalized yet.
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(add_report_request, user=user)
        create_report(add_report_request)
        review_request = factory.put('/api/v1/report/1')
        force_authenticate(review_request, user=user)
        response = report_detail(review_request, 1)
        self.assertEqual(response.status_code, 200)
        report = Report.objects.get(user_id=user)
        self.assertFalse(report.submitted)

    def test_report_submit_for_review_logged_in_already_finalized(self):
        """
        Test for when an authenticated user tries to submit for review a report
        that has already been finalized.
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(add_report_request, user=user)
        create_report(add_report_request)
        report = Report.objects.get(user_id=user)
        report.submitted = True
        report.save()
        review_request = factory.put('/api/v1/report/1')
        force_authenticate(review_request, user=user)
        response = report_detail(review_request, 1)
        self.assertEqual(response.status_code, 409)
