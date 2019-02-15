from datetime import date

#### Classes for policy, sections.

class Policy():

    def __init__(self):
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

class Section():
    
    def __init__(self, title="Section", html_description="", required=False,
                 auto_submit=False, fields={}):
        self.title = title
        self.html_description = html_description
        self.required = required
        self.auto_submit = auto_submit
        self.fields = fields
        self.rules = []

    def add_rule(self, title="Rule", rule=None, rule_break_text=""):
        rule = {
            "title": title,
            "rule": rule,
            "rule_break_text": rule_break_text,
        }
        self.rules.append(rule)

#### Policy configuration begin here

pol = Policy()

#### General
#### Section 0
general_section = Section(
    title="General Info",
    html_description="",
    fields={
        "destination": {"label": "Destination City", "field_type": "string"},
    }
)

general_section.add_rule(
    title="Destination city check",
    rule=lambda report, fields: fields['destination'] == "Timbuktu",
    rule_break_text="What did the cowboy say about Tim, his wild horse?"
)

pol.add_section(general_section)

#### Flight
#### Section 1
flight_section = Section(
    title="Flight Info",
    html_description="<p>Enter flight details here.</p>",
    fields={
        "international": {"label": "Is this an international flight?", "field_type": "boolean"},
        "departure_date": {"label": "Departure date", "field_type": "date"},
        "return_date": {"label": "Return date", "field_type": "date"},
        "fare": {"label": "Fare", "field_type": "decimal"},
        "layovers": {"label": "Transit wait", "field_type": "integer"},
        "fare_search_screenshot": {"label": "Screenshot of fare search", "field_type": "file"},
    }
)

flight_section.add_rule(
    title="Airline fare pre-approval check",
    rule=lambda report, fields: fields['fare'] < 500, 
    rule_break_text="Fares cannot be more than $500"
)

pol.add_section(flight_section)

#### Lodging
#### Section 2
lodging_section = Section(
    title="Hotel Info",
    html_description="<p>Enter hotel info here.\nPer diem rates can be found at "
                     "<a href='https://www.gsa.gov/travel/plan-book/per-diem-rates'>this link</a></p>",
    fields={
        "check-in_date": {"label": "Check-in date", "field_type": "date"},
        "check-out_date": {"label": "Check-out date", "field_type": "date"},
        "rate": {"label": "Per diem nightly rate", "field_type": "decimal"},
        "cost": {"label": "Total Cost", "field_type": "decimal"}
    }
)

def nightly_rate_check(report, fields):
    checkin_date = date(fields['checkin_date'])
    checkout_date = date(fields['checkout_date'])
    duration = checkout_date - checkin_date
    return fields['cost'] <= duration * fields['rate']

lodging_section.add_rule(
    title="Average nightly rate",
    rule=nightly_rate_check,
    rule_break_text="The average nightly rate cannot be more than the USGSA rate."
)

pol.add_section(lodging_section)

#### Local Transportation
#### Section 3
transport_section = Section(
    title="Local Transportation",
    html_description="<p>How much did you spend on local transportation, in total?</p>",
    fields={
        "duration": {"label": "How many days was your trip?", "field_type": "integer"},
        "cost": {"label": "Total cost", "field_type": "decimal"}
    }
)

transport_section.add_rule(
    title="Total cost check",
    rule=lambda report, fields: fields['cost'] <= fields['duration'] * 10,
    rule_break_text="Local transportation costs must be less than $10 per day, on average."
)

pol.add_section(transport_section)

#### Per Diem
#### Section 4
per_diem_section = Section(
    title="Per Diem",
    html_description="<p>Enter info about meals and incidentals here.\nPer diem rates can be found at "
                     "<a href='https://www.gsa.gov/travel/plan-book/per-diem-rates'>this link</a></p>",
    fields={
        "duration": {"label": "How many days was your trip?", "field_type": "decimal"},
        "rate": {"label": "What is the per diem rate for your destination?", "field_type": "decimal"},
        "cost": {"label": "Total Cost for meals and incidentals", "field_type": "decimal"}
    }
)

per_diem_section.add_rule(
    title="Per Diem Cost Check",
    rule=lambda report, fields: fields['cost'] <= fields['duration'] * fields['rate'],
    rule_break_text="The average cost per day for per diem expenses cannot be more than the rate specified by the USGSA."
)

pol.add_section(per_diem_section)
