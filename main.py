'''
    1. Shows all the courses that exist in the dir courses
    2. From the select one, loads all the questions saved
    3. Shows how many questions exists by that course
    4. Shows all the questions that exists by course
    5. Shows the % of exit from the user
'''

from exam_tester import QuestionManager as dv

# print(dv.data_validator.__subclasses__())
# print(dv.data_validator.EXISTING_COURSES)


# TODO: Add a validation to validate the imported questions if there are a load_questions.csv file and there exists row in it

a = dv.questions_loader(course=list(
    dv.data_validator.EXISTING_COURSES.keys())[0])
result_1 = a.initial_execution()
result_2 = a.import_new_questions()
print(a.working_course)
