import abc
from abc import ABC, abstractclassmethod
import pandas as pd
from sys import path
path.append("../exam_tester")
from exam_tester.io import io # noqa E402


class QuestionManager(ABC):
    """
    Class to validate all the imported and exported before working with it
    """
    # Dictionary with all the DataFrames imported
    data_imported = {
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
                        super().data_imported["imported_questions"] = data_exported

                    # Checks if the file has the modules and is not the history
                    elif file.lower().startswith("m"):
                        super().data_imported["existing_questions"] = self.__load_questions_to_class_variable(
                            data_to_load=data_exported,
                            variable_used=super().data_imported["existing_questions"])

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

    # TODO: Add to the MAIN a validation to execute this method if import questions has <1
    def import_new_questions(self) -> bool:
        """
        Method to import the valid questions into the internal CSV
        """

        # Handle if any error raises
        result_execution = False

        try:

            # List where all the valid imported questions are going to get listed
            valid_questions = [[cab for cab in super().data_imported["existing_questions"].columns]]

            # Executes the method to know if there are any valid questions to insert into the inner CSV
            if self.__check_valid_questions():

                # TODO: You have to iterate only the valid questions
                # Iterates all the new received questions
                for index, question_imported in super().data_imported["imported_questions"].iterrows():

                    # Adds to the list of valid questions the iterated question
                    data_question = [
                        self.__generate_code_for_question(question_imported["Module"], len(valid_questions) - 1),
                    ]
                    data_question.append(
                        [question_imported[header] for header in super().data_imported["imported_questions"].columns])

                    # Drop the imported question from the datatable with all the questions imported
                    super().data_imported["imported_questions"].drop(index=index)

                    # Checks if there are any valid question to be imported

                    # Converts the list of values imported into a DataFrame
                    imported_questions = pd.DataFrame(columns=valid_questions[0], data=valid_questions[1:])

                    # Adds to the correct CSV all the questions
                    if not self.__load_valid_questions_into_df(df_with_valid_questions=imported_questions):
                        raise Exception("Error detected loading the valid data to the CSV")

                    # Updates the CSV with the non valid questions (wrong_loaded_questions.csv)
                    if not self.__load_invalid_questions_into_df(df_with_non_valid_imported_questions=
                                                                 imported_questions):
                        raise Exception("Error detected updating the invalid questions into wrong_loaded_questions.csv")

                    # Merge the existing DataFrame with all the existing questions with the valid ones
                    super().data_imported["existing_questions"] = pd.concat(super().data_imported["existing_questions"]
                                                                            , imported_questions)

        except Exception as Error:
            self.error = f"There has been an error loading the new questions into the Exam Tester.\nError:{Error}"

        else:
            result_execution = True

        finally:

            # Returns as a count the imported questions
            return len(valid_questions) - 1

    def __check_valid_questions(self) -> bool:
        """
        Method to validate if the new imported questions are valid to enter into the internal CSV

        Validations:
            1. Checks if all the expected fields are informed
            2. Checks if the imported has a CSV to get saved
            3. Checks if the question imported already exist in the internal CSV
        """

        # Fields to know if there are any valid questions
        super().data_imported["imported_questions"]["Valid"] = 1

        # Checks if the expected fields are informed
        # FIXME: The loc method doesn't know's if the column has data or not
        """
        for column in self.headers_expected_load_question:
            super().data_imported["imported_questions"].loc[
                super().data_imported["imported_questions"][column] == pd.isnull, "Valid"] = 0
        """

        # TODO: Improve the system to knows if the module is valid by m1 to module1 and not forcing that the module informet is the same as the filename
        # Checks if there are questions from non valid modules by looking all the
        # FIXME: It doesn't return the modules that only exists inside the imported questions
        non_existing_modules = list(
            set(super().data_imported["imported_questions"]["Module"].unique()) - set(super().EXISTING_COURSES[
                self.working_course]))

        # All the questions with non existing modules are marked as invalid
        for non_valid_module in non_existing_modules:
            super().data_imported["imported_questions"].loc[
                super().data_imported["imported_questions"]["Module"] == non_valid_module, "Valid"] = 0

        # TODO: Pending to implement the logic to discard all the invalid questions
        """
        # Checks if there are questions duplicated inside the register
        for index, register in super().data_imported["imported_questions"].loc[ super().data_imported["imported_questions"]["Valid"] == 1].iterrow(): # noqa
            # Checks if the iterated questions imported exists inside the inner csv with all the questions
            super().data_imported["imported_questions"].loc[ super().data_imported["imported_questions"]["Question"] == register["Question"], "Valid"] = 0
        """

        # Returns if there are any valid question
        return True if len(super().data_imported["imported_questions"].loc[
                               super().data_imported["imported_questions"]["Valid"] == 1]) > 0 else False

    def __generate_code_for_question(self, module: str, questions_inserted: int) -> str:
        """
        Method to calculate the ID used for the question. The ID is calculated by the max question and the module
        """
        pass

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
