from django.test import TestCase
from .policy import pol
from unittest import mock
import datetime

class PolicyTests(TestCase):
    report = {"key":"value"}

    def test_general_section_pre_post_trip_check(self):
        fields = {'after_trip':True}
        result = pol.sections[0].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "If you have already take the trip your request will require special approval by the administrator. You may skip the following 'Pre-trip Planning' section.")

    def test_pre_flight_section_fare_limit_domestic(self):
        fields = {'preferred_flight_fare':751,'international_flight':False}
        result = pol.sections[1].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "Fares for domestic flights over 750 USD require Conservancy pre-approval, even if other policy conditions have been met.")

    def test_pre_flight_section_fare_limit_international(self):
        fields = {'preferred_flight_fare':1651,'international_flight':True}
        result = pol.sections[1].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "Fares for international flights over 1,650 USD require Conservancy pre-approval, even if other policy conditions have been met.")

    def test_pre_flight_section_lowest_fare_check_less_than_zero(self):
        fields = {'lowest_fare_duration':10,'preferred_flight_duration':11,'lowest_fare':100,'preferred_flight_fare':1000}
        result = pol.sections[1].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "For the lowest fare you have provided, your maximum in-policy fare amount is 200 USD.")

    def test_pre_flight_section_lowest_fare_check_less_than_three(self):
        fields = {'lowest_fare_duration':10,'preferred_flight_duration':8,'lowest_fare':100,'preferred_flight_fare':1000}
        result = pol.sections[1].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "For the lowest fare you have provided, your maximum in-policy fare amount is 200 USD.")

    def test_pre_flight_section_lowest_fare_check_less_than_six(self):
        fields = {'lowest_fare_duration':10,'preferred_flight_duration':5,'lowest_fare':100,'preferred_flight_fare':1000}
        result = pol.sections[1].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "For the lowest fare you have provided, your maximum in-policy fare amount is 300 USD.")

    def test_pre_flight_section_lowest_fare_check_less_than_ten(self):
        fields = {'lowest_fare_duration':10,'preferred_flight_duration':2,'lowest_fare':100,'preferred_flight_fare':1000}
        result = pol.sections[1].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "For the lowest fare you have provided, your maximum in-policy fare amount is 450 USD.")

    def test_pre_flight_section_lowest_fare_check_other(self):
        fields = {'lowest_fare_duration':12,'preferred_flight_duration':1,'lowest_fare':100,'preferred_flight_fare':1000}
        result = pol.sections[1].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "For the lowest fare you have provided, your maximum in-policy fare amount is 700 USD.")

    def test_pre_flight_section_departure_date_too_late(self):
        fields = {'departure_date':'2019-03-13','screenshot_date':'2019-03-01'}
        result = pol.sections[1].rules[2]['rule'](self.report, fields)
        self.assertEqual(result, "Flights must be booked at least 14 days in advance.")

    @mock.patch('datetime.date')
    def test_pre_flight_section_departure_date_too_early(self, mocked_date):
        mocked_date.today = mock.Mock(return_value=datetime.date(2019,1,1))
        fields = {'departure_date':'2020-03-10','screenshot_date':'2019-03-01'}
        result = pol.sections[1].rules[2]['rule'](self.report, fields)
        self.assertEqual(result, "Flights must be booked no more than 365 days in advance.")

    def test_flight_info_section_fare_limit_domestic(self):
        fields = {'fare':751,'international_flight':False}
        result = pol.sections[2].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "Fares for domestic flights over 750 USD require Conservancy pre-approval, even if other policy conditions have been met.")

    def test_flight_info_section_fare_limit_international(self):
        fields = {'fare':1651,'international_flight':True}
        result = pol.sections[2].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "Fares for international flights over 1,650 USD require Conservancy pre-approval, even if other policy conditions have been met.")

    def test_flight_info_section_request_date(self):
        fields = {'return_date':'2018-01-01'}
        result = pol.sections[2].rules[1]['rule'](self.report, fields)
        self.assertEqual(result, "Reimbursement requests must be made within 90 days of the last day of travel.")
 
    def test_hotels_lodging_section_average_nightly_rate(self):
        fields = {'check_in_date':'2019-03-01','check_out_date':'2019-03-11','cost':1100,'per_diem_rate':100}
        result = pol.sections[3].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "The average nightly rate cannot exceed the U.S. GSA rate.")

    def test_other_expenses_section_per_diem_check(self):
        fields = {'rate':100,'full_days':3,'partial_days':2,'cost':451}
        result = pol.sections[5].rules[0]['rule'](self.report, fields)
        self.assertEqual(result, "You may only request a maximum of 450.0 USD for the rate and trip duration provided.")
