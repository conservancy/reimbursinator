
let newReport = {
	"title": "2018 Portland trip",
	"date_created": "2018-05-22T14:56:28.000Z",
	"submitted": false,
	"date_submitted": "0000-00-00T00:00:00.000Z",
	"sections": [{
			"id": 1,
			"completed": false,
			"title": "Flight Info",
			"html_description": "<p>Enter flight details here.</p>",
			"fields": {
				"international": {
					"label": "International flight",
					"type": "boolean",
					"value": ""
				},
				"travel_date": {
					"label": "Travel start date",
					"type": "date",
					"value": ""
				},
				"fare": {
					"label": "Fare",
					"type": "decimal",
					"value": ""
				},
				"lowest_fare_screenshot": {
					"label": "Lowest fare screenshot",
					"type": "file",
					"value": ""
				},
				"plane_ticket_invoice": {
					"label": "Plane ticket invoice PDF",
					"type": "file",
					"value": ""
				}
			},
			"rule_violations": []
		},
		{
			"id": 2,
			"completed": false,
			"title": "Hotel info",
			"html_description": "<p>If you used a hotel, please enter the details.</p>",
			"fields": {
				"total": {
					"label": "Total cost",
					"type": "decimal",
					"value": ""
				}
			},
			"rule_violations": []
		}
	]
}
