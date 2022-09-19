from exam_tester import data_validator as dv

# print(dv.data_validator.__subclasses__())
# print(dv.data_validator.EXISTING_COURSES)

a = dv.questions_loader(course=list(
    dv.data_validator.EXISTING_COURSES.keys())[0])
result_1 = a.initial_execution()
result_2 = a.import_new_questions()
print(a.working_course)
