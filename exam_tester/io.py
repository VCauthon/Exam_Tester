from abc import ABC, abstractclassmethod
from exam_tester.entity import question

class io(ABC):
    '''
    Super class with all the classes used to import and export data about the questions
    '''

    def __init__(self, course) -> None:
        '''
            Sets the necessary data to read the questions of courses
        '''
        super().__init__()
        self.course = course

    @abstractclassmethod
    def read_data(self) -> question:
        pass

    @abstractclassmethod
    def save_data(self) -> bool:
        pass