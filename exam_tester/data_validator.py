from abc import ABC, abstractclassmethod
from sys import path
path.append("../exam_tester")
from exam_tester.io import io

class data_validator(ABC):
    """
    Class to validate all the imported and exported before working with it
    """

    imported_questions = 0
    df_logs_from_course = None
    df_questions_from_course = None
    df_questions_to_import = None

    def __init__(self, course:str) -> None:
        # Makes the io accessible to the rest of the subclass
        self.io_obj = io

        # Initial list of all the files inside the project
        self.existing_courses = io.list_current_files()

        # Variables used during all executions
        self.working_course = course

        # Control variable
        self.error = "None errors detected in the process"

    @abstractclassmethod
    def initial_execution(self) -> bool:
        pass