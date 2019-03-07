from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from backend.models import Report
from users.models import CustomUser
from unittest.mock import Mock, patch
from datetime import date
from backend.views import *

class ReportTests(TestCase):

    def create_test_user(self, email, first, last, password):
        user = CustomUser.objects.create_user(username=email, email=email, first_name=first, last_name=last, password=password)
        return user

    def mock_report():
        r = Mock()
        r.report_pk = 1
        r.title = 'Report Title'
        r.date_created = '2019-03-01'
        r.date_submitted = '2019-03-01'
        r.submitted = False
        r.reference_number = '12345'
        return r

    def setUp(self):
        self.test_user_1 = self.create_test_user('one@one.com', 'One', 'Mr. One', '1password')
        self.test_user_1.save()
 
    def test_create_report_logged_in(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(request, user=user)
        response = create_report(request)
        self.assertEqual(response.status_code, 200)
        report = Report.objects.get(user_id=user)
        self.assertEqual(report.title, 'Test Report')

    def test_create_report_logged_out(self):
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
