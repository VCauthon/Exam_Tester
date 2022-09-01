from abc import ABC, abstractclassmethod
from exam_tester.entities import question

class io(ABC):
    '''
    Super class with all the classes used to import and export data about the questions
    '''

    def __init__(self, course: dict) -> None:
        '''
            Sets the necessary data to read the questions of courses
        '''
        super().__init__()
        self.course = course
        self.error_detected = "None errors detected in the process"

    @abstractclassmethod
    def read_data(self) -> list(question):
        '''
            Abstract method to read CSV and return a pandas with 
        '''
        pass

    @abstractclassmethod
    def save_data(self) -> bool:
        pass