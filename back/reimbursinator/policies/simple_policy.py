# simple_policy.py
from datetime import date


#TODO:
# - For the rules, should one refer to fields by 'section.fields.x' or by the section name eg. 'general_section.fields.x'?


#### General
#### Section 0
general_section = Section(
	title = "General Info",
	html_description = "",
	fields = {
		"destination": {"label": "Destination City", "type": "string"}
	}
)

general_section.add_rule(
	title = "Destination city check",
	rule = lambda report, section:
		if section.fields.destination == "Timbuktu":
			return True
		else:
			return False
	,
	rule_break_text = "What did the cowboy say about Tim, his wild horse?"
)



#### Flight
#### Section 1
flight_section = Section(
	title = "Flight Info",
	html_description = "<p>Enter flight details here.</p>",
	fields = {
		"international": {"label": "Is this an international flight?", "type": "boolean"},
		"departure_date": {"label": "Departure date", "type": "date"},
		"return_date": {"label": "Return date", "type": "date"},
		"fare": {"label": "Fare", "type": "decimal"},
	}
)

flight_section.add_rule(
	title = "Airline fare pre-approval check",
	rule = lambda report, section:
		return section.fields.fare < 500
	, 
	rule_break_text = "Fares cannot be more than $500"
)



#### Lodging
#### Section 2
lodging_section = Section(
	title = "Hotel Info",
	html_description = "<p>Enter hotel info here.\nPer diem rates can be found at <a href='https://www.gsa.gov/travel/plan-book/per-diem-rates'></a></p>",
	fields = {
		"check-in_date": {"label": "Check-in date", "type": "date"},
		"check-out_date": {"label": "Check-out date", "type": "date"},
		"rate": {"label": "Per diem nightly rate", "type": "decimal"},
		"cost": {"label": "Total Cost", "type": "decimal"}
	}
)

section.add_rule(
	title = "",
	rule = lambda report, section:
		check-in_date = date(section.fields.check-in_date)
		check-out_date = date(section.fields.check-out_date)
		duration = check-out_date - check-in_date
		return section.fields.cost <= duration * section.fields.rate
	,
	rule_break_text = "The average nightly rate cannot be more than the USGSA rate."
)




#### Local Transportation
#### Section 3
transport_section = Section(
	title = "Local Transportation",
	html_description = "<p>How much did you spend on local transportation, in total?</p>",
	fields = {
		"duration": {"label": "How many days was your trip?", "type": "decimal"},
		"cost": {"label": "Total cost", "type": "decimal"}
	}
)

transport_section.add_rule(
	title = "Total cost check",
	rule = lambda report, section:
		return section.fields.cost <= section.fields.duration * 10
	,
	rule_break_text = "Local transportation costs must be less than $10 per day, on average."
)




#### Per Diem
#### Section 4
per_diem_section = Section(
	title = "Per Diem",
	html_description = "<p>Enter info about meals and incidentals here.\nPer diem rates can be found at <a href='https://www.gsa.gov/travel/plan-book/per-diem-rates'></a></p>",
	fields = {
		"duration": {"label": "How many days was your trip?", "type": "decimal"},
		"rate": {"label": "What is the per diem rate for your destination?", "type": "decimal"},
		"cost": {"label": "Total Cost for meals and incidentals", "type": "decimal"}
	}
)

per_diem_section.add_rule(
	title = "Per Diem Cost Check",
	rule = lambda report, section:
		return section.fields.cost <= section.fields.duration * section.fields.rate
	,
	rule_break_text = "The average cost per day for per diem expenses cannot be more than the rate specified by the USGSA."
)



'''
Section(
	title = "",
	html_description = "<p></p>",
	fields = {
		"": {"label": "", "type": ""}
	}
)

section.add_rule(
	title = "",
	rule = lambda report, section: return boolean_statement,  
	rule_break_text = ""
)

#// or, for a rule which doesn’t apply to a specific section...
#//
#// add_general_rule(...) 
'''
