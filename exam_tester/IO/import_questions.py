from sys import path
path.append("../exam_tester")

from exam_tester import io
from exam_tester.entity import question

class import_questions(io):
    '''
        1. Import new questions saved in the main dir
        2. Import all the saved questions and turn it into question objects
        3. Import all missed questions

            FORMAT > CSV: Module;Question;C_Answer,W_Answer##W_Answer2##W_Answer3;

            IMPORT NEW QUESTIONS
            IMPORT EXISTING QUESTION

            DATA FLOW > 
                1.Import CSV to PANDAS
                2.Search the questions you are gonna use
                3.Convert the results in questions.py
    '''

    def read_data(self) -> question:
        pass