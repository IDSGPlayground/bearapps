from lettuce import *
from store.models import User, User_Apps


@step('Given I log into the browse page and matlab has not been requested')
def make_a_member():
    new_student = new User(name = 'test', password = 'password', SID = 12345678910, user_type = 'GENERAL')
    new_student.save()
    world.student_var = new_student


@step('When I request matlab')
def request_app():
    sample_app = new User_Apps(name = 'Matlab', status = 'AVAILABLE')
    sample_app.user = world.student_var
    sample_app.status = "REQUESTED"
    world.app_var = sample_app


@step('I should see the status for matlab as REQUESTED')
def check():
    assert world.app_var.status == REQUESTED:
        world.student_var.delete()
        world.app_var.delete()
