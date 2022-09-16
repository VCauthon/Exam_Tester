from re import A
from sys import path
path.append("../../exam_tester")
import data_validator
import pandas as pd

class questions_loader(data_validator):
    
    
    def __init__(self, course:str) -> None:
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
            for file in super().existing_courses[super().working_course]:
                
                file_iterated_path = super().existing_courses[super().working_course][file]

                # Checks if the file has a valid extension
                if super().io.validate_file_extension(path=file_iterated_path, ext=".csv"):

                    data_exported = pd.read_csv(file_iterated_path)

                    # Checks if the file has the new questions to load
                    if file == "load_questions":
                        super().data_imported["imported_questions"] = data_exported

                    # Checks if the file has the modules and is not the history
                    elif file.lower().startswith("m"):
                        super().data_imported["existing_questions"] = self.__load_questions_to_class_variable(data_to_load= data_exported, \
                                variable_used=super().data_imported["existing_questions"])
        
        # If anything ocurred saves the error detected
        except Exception as error:
            super().error = f"There has been an error importing the file from {path} because of the following error.\nError:{error} \n IOError:{super().io.error}"
        
        else:
            result_execution = True

        finally:
            return result_execution


    def import_questions_detected():
        # Execute the check if question is valid and generate code for question
        # Return the imported questions and the missed ones
        pass


    def __check_if_question_is_valid():
        # Checks if all the fields are informed
        # Checks if there is any question that has the same question and answer
        # All the valid questions has to be append to the correct module
        # All the invalid questions has to be saved again to the load_questions.csv
        pass


    def __generate_code_for_question():
        # module and number question
        pass


    def __load_questions_to_class_variable(self, data_to_load:pd, variable_used:pd) -> pd:

        """
        Method to knows if there is a merge need it or not
        """

        if super().variable_used is not None:

            # Merge the existing variable with the new data
            return pd.concat([variable_used, data_to_load])

        # Checks if the variable where all the questions imported doesn't have data
        else:
            # Initialize the variable with new data
            return data_to_load