from typing import final
import pandas as pd
import os

class io:
    """
    Class to manage all the files inside the project
    """

    # Class variable to check if anything ocurred
    error = "None errors detected in the process"

    def list_courses() -> dict:
        """
        List all the files for every course
        """

        existing_courses = {}
        root_path_courses = "./exam_tester/courses"

        for course in os.listdir(root_path_courses):

            # Adds the course inside the returned dictionary
            course_iterated = os.path.join(root_path_courses, course)
            existing_courses[course] = {
                "path":course_iterated,
                "files": {}
            }

            for module in filter(lambda file: io.validate_file_extension(path=file, ext=".csv"), os.listdir(course_iterated)):
            
                # Appends inside the course entry the module
                existing_courses[course]["files"][os.path.splitext(module)[0]] = os.path.join(course_iterated, module)

        return existing_courses


    def import_csv_to_df(path:str) -> pd:
        """
        Import the received CSV into a DataFrame
        """

        data_imported = None

        try:

            # Checks if the file does exist and creates the imports it
            if io.check_file_exist(path):
                data_imported = pd.read_csv(path, sep=";")
            
            else:
                raise Exception("The file doesn't exists exist")
        
        # If anything ocurred saves the error detected
        except Exception as error:
            io.error = f"There has been an error importing the file {path} because of the following error.\nError:{error}"
        
        finally:
            return data_imported


    def export_df_to_csv(path:str) -> bool:
        """
        Export the received DataFrame into a CSV
        """
        pass


    def append_df_into_csv(path:str, df:pd) -> bool:
        """
        Append new data into to the existing CSV
        """
        pass


    def create_csv(path:str) -> bool:
        """
        Create a new empty file
        """
        result_execution = False

        # Tries to create the file
        try:

            # Checks if the file doesn't exist and creates the file
            if not io.check_file_exist(path):
                open(file=path, mode="w")
            
            # Detects if the file already exist
            else:
                raise Exception("The already exist")
        
        # If anything ocurred saves the error detected
        except:
            io.error = f"An error creating the file '{path}' has ocurred"

        # Checks if the process ended correctly
        else:
            result_execution = True
        
        finally:
            return result_execution


    def validate_file_exist(path:str) -> bool:
        """
        Checks if the path exist
        """
        return os.path.exists(path)


    def validate_file_extension(path:str, ext:str) -> bool:
        """
        Checks if the path has an specific extension
        """
        return os.path.splitext(path)[1] == ext
