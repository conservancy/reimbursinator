from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from backend.models import Report
from users.models import CustomUser
from unittest.mock import MagicMock, Mock, patch
from datetime import date
from backend.views import *
from .policy import pol
from decimal import Decimal
import json

class BackendTests(TestCase):

    # Set up functions
    ##################

    def create_test_user(self, email, first, last, password):
        """
        Create a test user and return it.
        """
        user = CustomUser.objects.create_user(username=email, email=email, first_name=first, last_name=last, password=password)
        return user

    def setUp(self):
        """
        Create a couple test users and save them in the database.
        """
        self.test_user_1 = self.create_test_user('one@one.com', 'One', 'Mr. One', '1password')
        self.test_user_1.save()
        self.test_user_2 = self.create_test_user('two@two.com', 'Two', 'Mr. Two', '1password')
        self.test_user_2.save()

    # Report-related Tests
    ######################

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
        response = report_detail(request)
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

    def test_report_finalize_logged_out(self):
        """
        Test for when an unauthenticated user tries to finalize a report.
        """
        factory = APIRequestFactory()
        request = factory.put('/api/v1/report/1/final')
        response = finalize_report(request, 1)
        self.assertEqual(response.status_code, 401)

    def test_report_finalize_wrong_owner(self):
        """
        Test for when an authenticated user tries to finalize someone else's report.
        """
        factory = APIRequestFactory()

        # Create a report for user One
        add_report_1_request = factory.post('/api/v1/report', {'title':'One\'s Report', 'reference':'12345'})
        force_authenticate(add_report_1_request, user=self.test_user_1)
        create_report(add_report_1_request)

        # Create a report for user Two
        add_report_2_request = factory.post('/api/v1/report', {'title':'Two\'s Report', 'reference':'12345'})
        force_authenticate(add_report_2_request, user=self.test_user_2)
        create_report(add_report_2_request)
        
        # Try finalizing user Two's report with user One
        request = factory.put('/api/v1/report/2/final')
        force_authenticate(request, user=self.test_user_1)
        response = finalize_report(request, 2)
        self.assertEqual(response.status_code, 401)
 
    def test_report_finalize_logged_in_not_finalized(self):
        """
        Test for when an authenticated user tries to finalize a report
        that has not been finalized yet.
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(add_report_request, user=user)
        create_report(add_report_request)
        review_request = factory.put('/api/v1/report/1/final')
        force_authenticate(review_request, user=user)
        response = finalize_report(review_request, 1)
        self.assertEqual(response.status_code, 200)
        report = Report.objects.get(user_id=user)
        self.assertTrue(report.submitted)

    def test_report_finalize_logged_in_already_finalized(self):
        """
        Test for when an authenticated user tries to finalize a report
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
        review_request = factory.put('/api/v1/report/1/final')
        force_authenticate(review_request, user=user)
        response = finalize_report(review_request, 1)
        self.assertEqual(response.status_code, 409)

    def test_report_get_report_logged_in(self):
        """
        Test for when an authenticated user tries to view a report.
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(add_report_request, user=user)
        create_report(add_report_request)
        get_request = factory.get('/api/v1/report/1')
        force_authenticate(get_request, user=user)
        response = report_detail(get_request, 1)
        self.assertEqual(response.status_code, 200)
        report = Report.objects.get(user_id=user)
        # Check that the json response contains the title of the report we want
        j = json.loads(response.content.decode("utf-8", "strict"))
        self.assertEqual(report.title, j['title'])

    def test_report_delete_report_logged_in(self):
        """
        Test for when an authenticated user tries to delete a report.
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'Test Report', 'reference':'12345'})
        user = CustomUser.objects.get(email='one@one.com')
        force_authenticate(add_report_request, user=user)
        create_report(add_report_request)
        delete_request = factory.delete('/api/v1/report/1')
        force_authenticate(delete_request, user=user)
        response = report_detail(delete_request, 1)
        self.assertEqual(response.status_code, 200)
        reports = Report.objects.filter(user_id=user)
        self.assertEqual(len(reports), 0)

    def test_user_owns_report_true(self):
        """
        Test when a user owns a report
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'One\'s Report', 'reference':'12345'})
        force_authenticate(add_report_request, user=self.test_user_1)
        create_report(add_report_request)
        self.assertTrue(user_owns_report(self.test_user_1, 1))

    def test_user_owns_report_false(self):
        """
        Test when a user doesn't own a report
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'One\'s Report', 'reference':'12345'})
        force_authenticate(add_report_request, user=self.test_user_1)
        create_report(add_report_request)
        self.assertFalse(user_owns_report(self.test_user_2, 1))

    # Section-related Tests
    #######################

    @patch('backend.views.get_fields', Mock(return_value={}))
    def test_get_sections(self):
        """
        Test gettings sections for a report.
        """
        report = Report.objects.create(
            user_id=self.test_user_1,
            title="Report Title",
            date_created=timezone.now(),
            reference_number="1234"
        )
        report.save()
        section_0 = Section.objects.create(
            report_id=report,
            auto_submit=False,
            required=False,
            completed=False,
            title='Section Zero',
            html_description='<p>Description zero</p>',
            number=0
        )
        section_0.save()
        section_1 = Section.objects.create(
            report_id=report,
            auto_submit=False,
            required=False,
            completed=False,
            title='Section One',
            html_description='<p>Description one</p>',
            number=1
        )
        section_1.save()
        expected = {
            'sections': [
                {
                    'completed': False,
                    'html_description': '<p>Description zero</p>',
                    'id': 1,
                    'rule_violations': [],
                    'title': 'Section Zero'
                },
                {
                    'completed': False,
                    'html_description': '<p>Description one</p>',
                    'id': 2,
                    'rule_violations': [],
                    'title': 'Section One'
                }
            ]
        } 
        result = get_sections(1)
        self.assertEqual(expected, result)

    def test_user_owns_section_true(self):
        """
        Test when a user owns a section
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'One\'s Report', 'reference':'12345'})
        force_authenticate(add_report_request, user=self.test_user_1)
        create_report(add_report_request)
        report = Report.objects.get(id=1)
        section = Section.objects.create(report_id=report, auto_submit=False, required=False, completed=False, title='Section Title', html_description='<p>Description.</p>', number=0)
        section.save()
        section_id = section.id
        self.assertTrue(user_owns_section(self.test_user_1, section_id))

    def test_user_owns_section_false(self):
        """
        Test when a user doesn't own a section
        """
        factory = APIRequestFactory()
        add_report_request = factory.post('/api/v1/report', {'title':'One\'s Report', 'reference':'12345'})
        force_authenticate(add_report_request, user=self.test_user_1)
        create_report(add_report_request)
        report = Report.objects.get(id=1)
        section = Section.objects.create(report_id=report, auto_submit=False, required=False, completed=False, title='Section Title', html_description='<p>Description.</p>', number=0)
        section.save()
        section_id = section.id
        self.assertFalse(user_owns_section(self.test_user_2, section_id))

    @patch('backend.models.Field.objects.filter')
    def test_section_complete_true(self, mocked):
        """
        Test if a section has been completed.
        """
        mocked.return_value = [
            Mock(completed=True),
            Mock(completed=False),
            Mock(completed=False)
        ]
        self.assertTrue(section_complete(1))

    @patch('backend.models.Field.objects.filter')
    def test_section_complete_false(self, mocked):
        """
        Test if a section has been completed.
        """
        mocked.return_value = [
            Mock(completed=False),
            Mock(completed=False),
            Mock(completed=False)
        ]
        self.assertFalse(section_complete(1))

    # Field-related Tests
    #####################

    def test_get_fields(self):
        """
        Test gettings fields for a section.
        """

        self.maxDiff = 5000
        # create sample report
        report = Report.objects.create(
            user_id=self.test_user_1,
            title="Report Title",
            date_created=timezone.now(),
            reference_number="1234"
        )
        report.save()

        # create sample section
        section_0 = Section.objects.create(
            report_id=report,
            auto_submit=False,
            required=False,
            completed=False,
            title='Section Zero',
            html_description='<p>Description zero</p>',
            number=0
        )
        section_0.save()

        # create sample fields
        field_0 = Field.objects.create(
            section_id=section_0,
            field_name='boolean',
            label='A boolean',
            number=0,
            field_type='boolean',
            completed=True,
            data_bool=True
        )
        field_0.save()
        field_1 = Field.objects.create(
            section_id=section_0,
            field_name='decimal',
            label='A decimal',
            number=1,
            field_type='decimal',
            completed=True,
            data_decimal=10.1
        )
        field_1.save()
        field_2 = Field.objects.create(
            section_id=section_0,
            field_name='date',
            label='A date',
            number=2,
            field_type='date',
            completed=True,
            data_date=date(2019,3,1)
        )
        field_2.save()
        field_3 = Field.objects.create(
            section_id=section_0,
            field_name='file',
            label='A file',
            number=3,
            field_type='file',
            completed=True,
            data_file='uploads/2019/03/01/file.jpg'
        )
        field_3.save()
        field_4 = Field.objects.create(
            section_id=section_0,
            field_name='string',
            label='A string',
            number=4,
            field_type='string',
            completed=True,
            data_string='string data'
        )
        field_4.save()
        field_5 = Field.objects.create(
            section_id=section_0,
            field_name='integer',
            label='An integer',
            number=5,
            field_type='integer',
            completed=True,
            data_integer=10
        )
        field_5.save()
        expected = {
            'fields': [
                {
                    'field_name': 'boolean',
                    'field_type': 'boolean',
                    'label': 'A boolean',
                    'value': True
                },
                {
                    'field_name': 'decimal',
                    'field_type': 'decimal',
                    'label': 'A decimal',
                    'value': Decimal('10.10')
                },
                {
                    'field_name': 'date',
                    'field_type': 'date',
                    'label': 'A date',
                    'value': '{}'.format(date(2019,3,1))
                },
                {
                    'field_name': 'file',
                    'field_type': 'file',
                    'label': 'A file',
                    'value': 'file.jpg'
                },
                {
                    'field_name': 'string',
                    'field_type': 'string',
                    'label': 'A string',
                    'value': 'string data'
                },
                {
                    'field_name': 'integer',
                    'field_type': 'integer',
                    'label': 'An integer',
                    'value': 10
                }
            ]
        }
        result = get_fields(1)
        self.assertEqual(expected, result)

    def generate_test_fields(self):
        test_boolean = models.BooleanField(default=False)
        test_boolean = True
        test_decimal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
        test_decimal = 100.10
        test_date = models.DateField(null=True, blank=True)
        test_date = date(2019,3,1)
        test_file = MagicMock()
        test_file.__str__.return_value = '/path/to/the/file.jpg'
        test_string = models.TextField(default='', blank=True)
        test_string = 'Some String'
        test_integer = models.IntegerField(default=0, blank=True)
        test_integer = 100
        fields = [
            {'field_name':'boolean', 'value':test_boolean, 'field_type':'boolean'},
            {'field_name':'decimal', 'value':test_decimal, 'field_type':'decimal'},
            {'field_name':'date', 'value':'{}'.format(test_date), 'field_type':'date'},
            {'field_name':'file', 'value':'{}'.format(test_file), 'field_type':'file'},
            {'field_name':'string', 'value':'{}'.format(test_string), 'field_type':'string'},
            {'field_name':'integer', 'value':test_integer, 'field_type':'integer'}
        ]
        return fields

    def test_generate_named_fields_for_section(self):
        """
        Test the generation of key-value dictionary from fields.
        """
        test_fields = self.generate_test_fields()
        result = generate_named_fields_for_section(test_fields)
        self.assertEqual(result, {
            'boolean':True,
            'decimal':100.10,
            'date':'2019-03-01',
            'file':'/path/to/the/file.jpg',
            'string':'Some String',
            'integer':100
        })
