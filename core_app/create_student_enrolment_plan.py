### TESTING GIT CHANGES WITH NEW BRANCH
from .models import *
from .progress_parser import parse_progress_report
#####
# {
#     template: {
#         <YEAR> : {
#         <SEMESTER> : {
#             <UNIT ID> : { name: <NAME>, credits: <CREDIT WORTH> }
#             }
#         }
#     }
#     plan: {
#         <YEAR> : {
#             <SEMESTER> : {
#                 <UNIT ID> : {
#                          name: <NAME>, credits: <CREDIT WORTH>, attempts: <PREV. ATTEMPTS>
#                 }
#             }
#         }
#     }
# }

def determine_unit_progress(unit_set):
    '''
    attempt_dict = {
        id: <>
        info: {
            status: <>
            attempts: <>
        }
    }
    @Params: All units student has done.
    @Return: a dict object, with unit as key and number of attempts as value.
    '''

    attempt_dict = {}

    for id, info in unit_set.items():

        if attempt_dict[id] == None:
            attempt_dict['id'] = id
            attempt_dict[id]['attempts'] = 0

        if info['status'] != 'PASS':
            attempt_dict[id]['status'] = False
        else:
            attempt_dict['status'] = True

        attempt_dict[id]['attempts'] += 1

    return attempt_dict


with open('/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/StudentProgressReport-17080170-27_Mar_2017.pdf', 'rb') as fp:
    json_parsed_file = parse_progress_report(fp)

student = Student.objects.get(StudentID=json_parsed_file['id'])
unit_attempts = determine_unit_progress(json_parsed_file['units'])

for unit_ID, unit_info in json_parsed_file['units'].items():

    current_unit = Unit.object.get(UnitID=unit_ID)

    studentUnit = StudentUnit(StudentID=student.StudentID, UnitID=unit_ID)
    studentUnit.Attempts = unit_attempts[unit_ID]['attempts']
    studentUnit.Status = unit_attempts[unit_ID]['status']
    # studentUnit.Status = unit_info['status']

    # studentUnit.Attempts = unit_info['']


