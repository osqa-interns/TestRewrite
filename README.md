# TestRewrite
This repo includes test scripts for Openstax Tutor.

Go to [Openstax Testrail](https://openstax.testrail.net/index.php?/suites/view/268&group_by=cases:section_id&group_order=asc) for corresponding test cases 

All corresponding test cases are also available on [Trello](https://trello.com/b/5TDvzN8l/test-rewrite) 

## Installation/Configuration
Go to this [repo](https://github.com/openstax/test-automation/tree/master/tutor) and follow the steps in README.md to set up a virutal environment 

## Running tests locally 
Activate the virtual environment created in the previous step 
Open terminal window and navigate to the repo folder 
`LOCALRUN=true TEACHER_USER=example TEACHER_PASSWORD=example SERVER_URL="tutor-qa.openstax.org" python -m pytest -v test_file_name`

## Clean up assignments 
If there are too many assignments created on a teacher's calendar and you want to delete some of them, run [test_clean_up_calendar.py](https://) and select the type of assignment you delete.






