from sys import path
path.append("../../exam_tester")
import data_validator

class logs_loader(data_validator):
    
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
            for file in super().existing_courses:
                
                # Checks if the file is from the logs

                # Checks if the file isn't from the logs

                # New file where the data
                pass

            pass
        
        # If anything ocurred saves the error detected
        except Exception as error:
            super().error = f"There has been an error importing the file from {path} because of the following error.\nError:{error} \n IOError:{super().io.error}"
        
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