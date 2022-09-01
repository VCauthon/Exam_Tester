from abc import ABC, abstractclassmethod
import pandas as pd

# Internal modules of the program
from sys import path
path.append("../exam_tester")
from exam_tester.file_manager import file_manager as fg
from exam_tester.entities import question

class io(ABC):
    '''
    Super class with all the classes used to import and export data about the questions
    '''

    def __init__(self, course: dict) -> None:
        '''
            Sets the necessary data to read the questions of courses
        '''
        self.course = course
        self.error_detected = "None errors detected in the process"
        
    @abstractclassmethod
    def read_data(self, used_path: str) -> pd:
        '''
            Abstract method to read CSV and return a pandas with 
        '''
        pass

    @abstractclassmethod
    def save_data(self, list_questions: list(question)) -> bool:
        '''
            Abstract method to convert a list of questions into CSV
        '''
        pass

    def update_list_files(self) -> dict:
        """TODO
            Have to control what happens if the list_current_files is empty in the main
            The returned DICT have the next format
                0 COURSES
                    0 MODULE
                        PATH_QUESTIONS:
                        HISTORY: 

            ALL THE EMPTY FILES HAVE TO RETURN A NONE VARIABLE
        """
        return fg.list_current_files