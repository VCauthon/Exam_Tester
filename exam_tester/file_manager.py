from distutils.log import error
from msilib.schema import Directory
import os

class file_manager:
    '''
        1.Knows the existing courses
        2.Returns the existing modules of the course
        3.Creates the history file if doesn't exist
        4.Returns the history path of the course

    '''

    error = "None errors detected in the process"

    def list_current_files() -> dict:
        """
        Returns a dictionary with all the modules and questions exist by course
        """
        existing_courses = {}
        root_path_courses = "./exam_tester/courses"

        for course in os.listdir(root_path_courses):

            # Adds the course inside the returned dictionary
            course_iterated = os.path.join(root_path_courses, course)
            existing_courses[course] = {
                "path":course_iterated,
                "files": []
            }

            for module in filter(lambda file: file_manager.check_extension_file(path_file=file, extension=".csv"), os.listdir(course_iterated)):
                
                # Appends inside the course entry the module
                existing_courses[course]["files"].append(os.path.join(course_iterated, module))

        return existing_courses

    def create_csv(path_file: str) -> bool:
        """
        If the file doesn't exists it creates an empty CSV
        """
        result_execution = False

        # Tries to create the file
        try:

            # Checks if the file doesn't exist
            if not file_manager.check_file_exist(path_file):

                open(file=path_file, mode="w")

        except:
            file_manager.error = f"An error creating the file '{path_file}' has ocurred"

        else:
            result_execution = True
        

    def check_file_exist(path_file: str) -> bool:
        return os.path.exists(path_file)


    def check_extension_file(path_file: str, extension: str) -> bool:
        return os.path.splitext(path_file)[1] == extension