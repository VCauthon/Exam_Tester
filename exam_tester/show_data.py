import abc
from abc import ABC, abstractclassmethod

# Internal modules of the program
from sys import path
path.append("../exam_tester")
from exam_tester.entities import question # noqa E402


# Hello
class show_data(ABC):
    """
        Super class with all the classes used to show data in the terminal
    """

    def __init__(self) -> None:
        self.error_detected = "None errors detected in the process"
        self.questions_pandas = None

    # TODO: Pending to create a main function of the class
    def modes(self) -> dict:
        """
            Method to show all the existing process of the exam tester
        """
        pass

    # TODO: Pending to create a main function of the class
    def convert_df_to_question(self) -> list[question]:
        """
            Method to convert the received pandas into a list of questions
        """
        pass

    @abc.abstractmethod
    def execute(self) -> bool:
        """
            Abstract method to run the instanced process asked by the user
        """
        pass
