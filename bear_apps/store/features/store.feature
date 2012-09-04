Feature: Request an application

	Scenario: Gimme Matlab
		Given I log into the browse page and matlab has not been requested
		When I request matlab
		I should see the status for matlab as REQUESTED

Feature: Making an admin a member of all groups

	Scenario: Crowning an admin
		Given that I am an admin
		I should be a mamber of all existing groups and should not make any extraneous groups