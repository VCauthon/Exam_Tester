import abc
from abc import ABC, abstractclassmethod
import pandas as pd
from sys import path

path.append("../exam_tester")
from exam_tester.io import io  # noqa E402


class QuestionManager(ABC):
    """
    Class to validate all the imported and exported before working with it
    """

    imported_questions = pd.DataFrame
    existing_questions = pd.DataFrame

    # Dictionary with all the DataFrames imported
    data_used = {
        "logs_course": pd.DataFrame,
        "imported_questions": pd.DataFrame,
        # TODO: The imported_questions = 0 variable can be calculate by the own DataFrame (NEW COLUMN) # noqa
        "existing_questions": pd.DataFrame
    }

    # TODO: Resolve how to invoke IO without using self parameter
    # Initial list of all the files inside the project
    EXISTING_COURSES = io.list_courses()

    def __init__(self, course: str) -> None:
        # Makes the io accessible to the rest of the subclass
        self.io_obj = io()

        # Variables used during all executions
        self.working_course = course

        # Control variable
        self.error = "None errors detected in the process"

    @abc.abstractmethod
    def initial_execution(self) -> bool:
        pass


# TODO: Look how to move all the class to other object
class QuestionLoader(QuestionManager):

    def __init__(self, course: str) -> None:
        super().__init__(course)

        # Variable to set the expected headers for load_questions
        self.headers_expected_load_question = ["Module", "Question",
                                               "C_Answer", "W_Answer",
                                               "Source", "Detail_answer"]
        self.headers_expected_load_module = ["ID", "Module",
                                             "Question", "C_Answer",
                                             "W_Answer", "Source",
                                             "Detail_answer"]

        # Variables where all the questions are going to get saved
        self.imported_questions = pd.DataFrame
        self.existing_questions = pd.DataFrame

    def initial_execution(self) -> bool:
        """
        Initial execution to load all the imported and existing questions
        """

        # Handle if any error raises
        result_execution = False
        try:

            # Iterate all the dictionary following the key of the course
            for file in super().EXISTING_COURSES[self.working_course]["files"]:

                file_iterated_path = super().EXISTING_COURSES[
                    self.working_course]["files"][file]

                # Checks if the file has a valid extension
                if self.io_obj.validate_file_extension(
                        path=file_iterated_path,
                        ext=".csv") and (
                        file == "load_questions" or
                        file.lower().startswith("m")):

                    data_exported = pd.read_csv(file_iterated_path, sep=";")

                    # Checks if the file has the new questions to load
                    if file == "load_questions":
                        self.imported_questions = data_exported

                    # Checks if the file has the modules and is not the history
                    elif file.lower().startswith("m"):
                        super().existing_questions = self.__load_questions_to_class_variable(
                            data_to_load=data_exported,
                            variable_used=self.existing_questions)

            # Checks if the imported load_questions file has the proper headers
            if super().data_imported["imported_questions"] is not None and len(
                    super().data_imported["imported_questions"]) > 0:

                # Checks if all the headers are in the imported file
                if len(list(set(super().data_imported["imported_questions"].columns) -
                            set(self.headers_expected_load_module))) > 0:
                    # The process raise an error indicating the erroneous headers
                    showed_data = super().data_imported["imported_questions"].columns
                    raise Exception(
                        f"The file with the imported questions doesn't have the expected headers \n Has:{showed_data} "
                        f"\n Expected: {self.headers_expected_load_module}")

            # Checks if the imported questions from the inner csv file has the proper headers
            if super().data_imported["existing_questions"] is not None and len(
                    super().data_imported["existing_questions"]) > 0:

                # Checks if there are any differences between the headers of the imported CSV vs the expected headers
                if len(list(set(super().data_imported["existing_questions"].columns) -
                            set(self.headers_expected_load_question))) > 0:
                    # The process raise an error indicating the erroneous headers
                    showed_data = super().data_imported["existing_questions"].columns
                    raise Exception(
                        f"The file with the imported questions doesn't have the expected headers \n Has: {showed_data} "
                        f"\n Expected: {self.headers_expected_load_question}")

        # If anything ocurred saves the error detected
        except Exception as error:
            self.error = f"There has been an error importing the file from {path} because of the following error." \
                         f"\nError:{error} \n IOError:{self.io_obj.error}"

        else:
            result_execution = True

        finally:
            return result_execution

    def load_valid_imported_questions_to_system(self) -> int:
        """
        Method to import the valid questions into the internal CSV
        """

        valid_questions_imported = pd.DataFrame

        try:

            if self.__check_valid_imported_questions_exist() and self.__check_valid_imported_questions_exist():

                valid_questions_imported = self.__adds_id_column_to_df_imported_questions(
                    self.__return_imported_questions_by_validity(1))

                # Adds to the correct CSV all the questions
                if not self.__load_valid_questions_into_df(
                        df_with_valid_questions=valid_questions_imported):
                    raise Exception("Error detected loading the valid data to the CSV")

                # Updates the CSV with the non valid questions (wrong_loaded_questions.csv)
                if not self.__load_invalid_questions_into_df(df_with_non_valid_imported_questions=
                                                             self.__return_imported_questions_by_validity(0)):
                    raise Exception("Error detected updating the invalid questions into wrong_loaded_questions.csv")

                # Merge the existing DataFrame with all the existing questions with the valid ones
                self.existing_questions = pd. \
                    concat([self.existing_questions, valid_questions_imported])

        except Exception as Error:
            self.error = f"There has been an error loading the new questions into the Exam Tester.\nError:{Error}"

        finally:

            # Returns as a count the imported questions
            return len(valid_questions_imported)

    def __return_imported_questions_by_validity(self, validity: int) -> pd.DataFrame:
        # List where all the valid imported questions are going to get listed
        valid_questions = [[cab for cab in self.imported_questions.columns]]
        return self.imported_questions.loc[self.imported_questions["Valid"] == validity][valid_questions]

    def __adds_id_column_to_df_imported_questions(self, data_frame_in: pd.DataFrame) -> pd.DataFrame:
        """
        Method to add to the received list a column with all the ID
        """

        # Adds to the DF the column where all ID are going to get listed
        data_frame_in.insert(loc=0, column="ID", value="")

        # Calculate and adds the new values
        last_id_inner_questions = len(self.imported_questions)
        data_frame_in["ID"] = [i for i in range(last_id_inner_questions + 1, (last_id_inner_questions*2) + 1)]

        return data_frame_in

    def valid_questions_from_imported_file(self) -> bool:
        return len(self.imported_questions.loc[self.imported_questions["Valid"] == 1]) > 0

    # region Validations done before importing any new question to the inner csv files

    def __check_valid_imported_questions_exist(self) -> bool:
        """
        Method to validate if the new imported questions are valid to enter into the internal CSV

        Validations:
            - Checks if the imported has a CSV to get saved
            - Checks if the question imported already exist in the internal CSV
        """

        # Adds a column to mark the valid questions (all starts as valid)
        self.imported_questions["Valid"] = 1

        if self.__mark_imported_questions_with_invalid_module():
            self.__mark_imported_questions_duplicated()

        return self.valid_questions_from_imported_file()

    def __mark_imported_questions_with_invalid_module(self) -> bool:
        """
            Marks all the questions from the imported file (load_questions.csv) than has a module (column 1) that
            doesn't exist in the existing modules from the course selected.

            The existing modules are calculated based in the name of the inner csv file.
        """

        # Gets all the modules from the imported questions
        modules_from_imported_questions = list(self.imported_questions["imported_questions"]["Module"].unique())

        # Gets all non valid modules
        non_valid_modules = set(modules_from_imported_questions) - set(super().EXISTING_COURSES[self.working_course])

        for non_valid_module in non_valid_modules:
            self.imported_questions.loc[self.imported_questions["Module"] == non_valid_module, "Valid"] = 0

        return self.valid_questions_from_imported_file()

    def __mark_imported_questions_duplicated(self) -> bool:
        """
            Marks as invalid all the registers from the imported questions with the same question and module
        """

        for index, question in self.imported_questions.loc[self.imported_questions["Valid"] == 1].iterrows():
            # Checks if the iterated register has the same module and question
            if len(self.existing_questions.query(
                    f"Module == '{question['Module']}' & Question == '{question['Question']}'")) > 0:
                self.imported_questions.at[index, 'Value'] = 0

        return self.valid_questions_from_imported_file()

    # endregion

    def __load_valid_questions_into_df(self, df_with_valid_questions: pd) -> bool:
        """
        Has to search for every question the correct CSV where it has to save all the data
        """

        self.io_obj.validate_file_exist(path="")

    def __load_invalid_questions_into_df(self, df_with_non_valid_imported_questions: pd) -> bool:
        """
        Has to search create or update the wrong_loaded_questions
        """
        pass

    def __load_questions_to_class_variable(self, data_to_load: pd, variable_used: pd) -> pd:

        """
        Method to knows if there is a merge need it or not
        """

        if variable_used is not None:

            # Merge the existing variable with the new data
            return pd.concat([variable_used, data_to_load])

        # Checks if the variable where all the questions imported doesn't have data
        else:
            # Initialize the variable with new data
            return data_to_load


# TODO: Move the module to the other directory
class QuestionLogger(QuestionManager):

    def __init__(self, course: str) -> None:
        super().__init__(course)
        self.initial_execution()

    def initial_execution(self) -> bool:
        """
        Initial execution to load all the imported and existing questions
        """

        # Handle if any error raises
        result_execution = False
        try:

            # Iterate all the dictionary following the key of the course
            for file in super().EXISTING_COURSES:
                # Checks if the file is from the logs

                # Checks if the file isn't from the logs

                # New file where the data
                pass

            pass

        # If anything ocurred saves the error detected
        except Exception as error:
            self.error = f"There has been an error importing the file from {path} because of the following error." \
                         f"\nError:{error} \n IOError:{self.io_obj.error}"

        else:
            result_execution = True

        finally:
            return result_execution

    # TODO: Pending create the new variable
    def __append_data_into_df(self, data_new, data_load) -> bool:
        """
        Method to load new data to the final variable
        """
        # Checks if the variable where all the questions imported already has data

        # Merge the existing variable with the new data

        # Checks if the variable where all the questions imported doesn't have data

        # Initialize the variable with new data
