# Settings to import the data from the software
from sys import path
path.append("../exam_tester")
from exam_tester import io
from exam_tester.entities import question

# Import the module to search path
import os

class read_new_questions(io):
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


    #TODO You have to take in a account that in some questions there are fake break line (/n)
    def read_data(self) -> list(question):
        '''
        Method to convert CSV to question
        '''

        # Search if all the received path exists
        for file in super().courses.keys():
            if not os.path.exists(super().courses[file]):
                raise Exception("The process asked to import a file that doesn't exists")



        pass