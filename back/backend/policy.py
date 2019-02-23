from datetime import date

#### Classes for policy, sections. Do not edit these.
#####################################################

class Policy():
    """
    Represents the policy for the company/organization.
    """
    def __init__(self):
        """
        Creates a new Policy object.
        """
        self.sections = []

    def add_section(self, section):
        """
        Appends the specified section to the policy in order.

        section -- Section object to append.
        """
        self.sections.append(section)

class Section():
    """
    Represents a logical division of te policy, containing
    data fields for users to enter, and rules which
    apply to those fields.
    """
    def __init__(self, title="Section", html_description="", required=False, auto_submit=False, fields={}):
        """
        Creates a new Section object.

        title -- This is the name for the section the user sees.
        html_description -- This is html displayed beneath the title.
        required -- If True, user must complete before submitting.
        auto_submit -- Completing this section notifies the administrator.
        fields -- A python object of fields the user should enter.
        """
        self.title = title
        self.html_description = html_description
        self.required = required
        self.auto_submit = auto_submit
        self.fields = fields
        self.rules = []

    def add_rule(self, title="Rule", rule=None, rule_break_text=""):
        """
        Assigns a new rule to the section.

        title -- Administrative title for the rule.
        rule -- lambda expression which must evaluate true to pass the rule.
        rule_break_text -- Error message to show the user when rule is broken.
        """
        rule = {
            "title": title,
            "rule": rule,
            "rule_break_text": rule_break_text,
        }
        self.rules.append(rule)

pol = Policy()

#### Policy configuration begins here. Edit below this line.
############################################################

#### General
#### Section 0
general_section = Section(
    title="General Info",
    html_description="<p>Each section of this report is designed to guide you through the reimbursement process. Please read through each and answer as many questions as you can that apply to you.</p><p>Be sure to click 'Save' after completing each section. Your entered data will be saved as you progress. You may also receive feedback from sections regarding policy restrictions and special requirements.</p>",
    fields={
        "after_trip": {"number": 0, "label": "Have you taken this trip already?", "field_type": "boolean"},
    }
)

general_section.add_rule(
    title="Pre-trip / post-trip check",
    rule=lambda report, fields: "If you have already take the trip your request will require special approval by the administrator. You may skip the following 'Pre-trip Planning' section." if fields['after_trip'] else None
)

pol.add_section(general_section)

#### Pre-trip Planning
#### Section 1

planning_section = Section(
    title="Pre-trip Planning",
    html_description="<p>At least 14 days before buying tickets for your trip, take a screenshot of a flight search showing the least expensive fare available for the dates you need to travel. Include fares from multiple airlines if possible. This information will be used to calculate reimbursable fare amounts.</p>",
    fields={
        "departure_date": {"number": 0, "label": "Departure date", "field_type": "date"},
        "return_date": {"number": 1, "label": "Return date", "field_type": "date"},
	"screenshot": {"number": 2, "label": "Screenshot of least expensive ticket fare", "field_type": "file"},
	"screenshot_date": {"number": 3, "label": "Date of screenshot", "field_type": "date"},
        "lowest_fare": {"number": 4, "label": "Lowest fare", "field_type": "decimal"},
        "lowest_fare_duration": {"number": 5, "label": "Flight duration of lowest fare (hours)", "field_type": "decimal"},
        "preferred_flight_fare": {"number": 6, "label": "Fare of your preferred flight", "field_type": "decimal"},
        "preferred_flight_duration": {"number": 7, "label": "Flight duration of your preferred flight (hours)", "field_type": "decimal"},
	"international_flight": {"number": 8, "label": "Is this an international flight?", "field_type": "boolean"},
    }
)

def fare_limit_rule(report, fields):
    intl_flight = fields['international_flight']
    fare = fields['preferred_flight_fare']
    if intl_flight:
        if fare > 1650:
            return "Fares for international flights over 1,650 USD require Conservancy pre-approval, even if other policy conditions have been met."
    else:
        if fare > 750:
            return "Fares for domestic flights over 750 USD require Conservancy pre-approval, even if other policy conditions have been met."
    return None

planning_section.add_rule(title="Fare limits", rule=fare_limit_rule)

def lowest_fare_rule(report, fields):
    diff = fields['lowest_fare_duration'] - fields['preferred_flight_duration']
    lowest_fare = fields['lowest_fare']
    maximum = 0
    if diff <= 0:
        maximum = lowest_fare + 100
    elif diff <= 3:
        maximum = lowest_fare + 100
    elif diff <= 6:
        maximum = lowest_fare + 200
    elif diff <= 10:
        maximum = lowest_fare + 350
    else:
        maximum = lowest_fare + 600
    if fields['preferred_fare'] > maximum:
        return "For the lowest fare you have provided, your maximum in-policy fare amount is {} USD.".format(maximum)
    return None

planning_section.add_rule(title="Lowest fare check", rule=lowest_fare_rule)

def departure_date_limit_rule(report, fields):
    days_to_departure = date(fields['departure_date']) - date(fields['screenshot_date'])
    if days_to_departure < 14:
        return "Flights must be booked at least 14 days in advance."
    if days_to_departure > 365:
        return "Flights must be booked no more than 365 days in advance."
    return None

planning_section.add_rule(title="Departure date limit", rule=departure_date_limit_rule)
pol.add_section(planning_section)

#### Flight Info
#### Section 2

flight_section = Section(
    title="Flight Info",
    html_description="<p>Enter the details of your flight once you have made your purchase.</p>",
    fields={
        "departure_date": {"number": 0, "label": "Actual departure date", "field_type": "date"},
        "return_date": {"number": 1, "label": "Actual return date", "field_type": "date"},
        "fare": {"number": 2, "label": "Ticket fare", "field_type": "decimal"},
        "confirmation_screenshot": {"number": 3, "label": "Screenshot of confirmation of purchase", "field_type": "file"},
        "international_flight": {"number": 4, "label": "Was this an international flight?", "field_type": "boolean"},
    }
)

def actual_fare_limit_rule(report, fields):
    intl_flight = fields['international_flight']
    fare = fields['fare']
    if intl_flight:
        if fare > 1650:
            return "Fares for international flights over 1,650 USD require Conservancy pre-approval, even if other policy conditions have been met."
    else:
        if fare > 750:
            return "Fares for domestic flights over 750 USD require Conservancy pre-approval, even if other policy conditions have been met."
    return None

flight_section.add_rule(title="Fare limits", rule=actual_fare_limit_rule)

def request_date_rule(report, fields):
    now = date.today()
    last_travel = date(fields['return_date'])
    if now - last_travel > 90:
        return "Reimbursement requests must be made within 90 days of the last day of travel."
    return None

flight_section.add_rule(title="Request date", rule=request_date_rule)
pol.add_section(flight_section)

#### Hotels / Lodging
#### Section 3

lodging_section = Section(
    title="Hotel / Lodging",
    html_description="<p>Please submit a receipt from your hotel including both the total amount and the dates of your stay. Per diem rates can be found on <a href='https://www.gsa.gov/travel/plan-book/per-diem-rates' target='_blank'>the U.S. GSA website</a>.</p>",
    fields={
	"per_diem_rate": {"number": 0, "label": "USGSA Per diem rate", "field_type": "decimal"},
        "cost": {"number": 1, "label": "Total cost for lodging", "field_type": "decimal"},
        "check_in_date": {"number": 2, "label": "Check-in date", "field_type": "date"},
        "check_out_date": {"number": 3, "label": "Check-out date", "field_type": "date"},
        "invoice_screenshot": {"number": 4, "label": "Screenshot of invoice", "field_type": "file"},
    }
)

def nightly_rate_check(report, fields):
    checkin_date = date(fields['check_in_date'])
    checkout_date = date(fields['check_out_date'])
    duration = checkout_date - checkin_date
    if fields['cost'] > duration * fields['per_diem_rate']:
        return "The average nightly rate cannot exceed the U.S. GSA rate."
    return None

lodging_section.add_rule(title="Average nightly rate", rule=nightly_rate_check)

pol.add_section(lodging_section)

#### Local Transportation
#### Section 4

transport_section = Section(
    title="Local Transportation",
    html_description="<p>This amount includes taxis, uber, and public transportation.</p>",
    fields={
        "cost": {"number":0, "label": "Total cost of local transportation", "field_type": "decimal"}
    }
)

pol.add_section(transport_section)

#### Per Diem and Other Expenses
#### Section 5

per_diem_section = Section(
    title="Per Diem and Other Expenses",
    html_description="<p>Your per diem allowance is used to cover meals and incidental expenses. The rate for your travel destination can be found on the following websites:</p><ul><li><a href='https://www.gsa.gov/perdiem' target='_blank'>US General Serices Administration</a> for travel in the United States</li><li><a href='https://aoprals.state.gov/web920/per_diem.asp' target='_blank'>US Department of State</a> for travel outside the United States</li></ul><p>You may request up to 100% of the listed rate for a full day of travel, or 75% for a partial day of travel.",
    fields={
	"rate": {"number":0, "label": "Per diem rate", "field_type": "decimal"},
        "full_days": {"number":1, "label": "Number of full days of travel", "field_type": "integer"},
        "partial_days": {"number":2, "label": "Number of partial days of travel", "field_type": "integer"}, 
	"cost": {"number":3, "label": "Total Cost for meals and incidentals", "field_type": "decimal"}
    }
)

def incidentals_rule(report, fields):
    rate = fields['rate']
    maximum = fields['full_days'] * rate + fields['partial_days'] * .75 * rate
    if fields['cost'] > maximum:
        return "You may only request a maximum of {} USD for the rate and trip duration provided.".format(maximum)
    return None

per_diem_section.add_rule(title="Per diem check", rule=incidentals_rule)

pol.add_section(per_diem_section)

#### Payment Option - Paypal
#### Section 6

paypal_section = Section(
    title="Payment Option - Paypal",
    html_description="<p>Complete this section if you wish to be reimbursed via Paypal. This is the preferred reimbursement method of Software Freedom Conservancy.</p>",
    fields={
        "paypal_email": {"number":0, "label":"Email address used with Paypal", "field_type":"string"},
        "preferred_currency": {"number":1, "label":"Preferred currency", "field_type":"string"},
    }
)

pol.add_section(paypal_section)

#### Payment Option - Check
#### Section 7

check_section = Section(
    title="Payment Option - Check",
    html_description="<p>Complete this section if you wish to be reimbursed in USD via check sent by mail.</p>",
    fields={
        "address_1": {"number":0, "label":"Street address", "field_type":"string"},
        "address_2": {"number":1, "label":"Street address 2", "field_type":"string"},
        "city": {"number":2, "label":"City", "field_type":"string"},
        "state": {"number":3, "label":"State", "field_type":"string"},
        "zip": {"number":4, "label":"Zip code", "field_type":"string"},
    }
)

pol.add_section(check_section)

#### Payment Option - Bank Wire
#### Section 8

wire_section = Section(
    title="Payment Option - Bank Wire",
    html_description="<p>Complete this section if you wish to be wired the amount to your bank in your local currency. Please fill in as much of the following information as is possible. Please refer to the <a href='https://sfconservancy.org/projects/policies/conservancy-travel-policy.html' target='_blank'>SFC travel policy</a> for additional bank information required for certain countries.</p>",
    fields={
        "name": {"number":0, "label":"Full name of account holder", "field_type":"string"},
        "address_1": {"number":1, "label":"Street address", "field_type":"string"},
        "address_2": {"number":2, "label":"Street address 2", "field_type":"string"},
        "city": {"number":3, "label":"City", "field_type":"string"},
        "state": {"number":4, "label":"State", "field_type":"string"},
        "zip": {"number":5, "label":"Zip code", "field_type":"string"},
        "account": {"number":6, "label":"Account number", "field_type":"string"},
        "currency": {"number":7, "label":"Preferred currency", "field_type":"string"},
        "bank_name": {"number":8, "label":"Bank name", "field_type":"string"},
        "bank_address": {"number":9, "label":"Bank address", "field_type":"string"},
        "routing_number": {"number":10, "label":"Bank ACH/ABA routing number (US) or SWIFT/BIC code (non-US)", "field_type":"string"},
        "additional_info": {"number":11, "label":"Additional information (see SFC policy)", "field_type":"string"},
    }
)

pol.add_section(wire_section)

