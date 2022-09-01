
class file_manager:
    '''
        1.Knows the existing courses
        2.Returns the existing modules of the course
        3.Creates the history file if doesn't exist
        4.Returns the history path of the course

    '''

    error = "None errors detected in the process"

    def list_current_files(self) -> dict:
        pass

    def create_csv(self, path_file: str) -> bool:
        pass

    def check_file_exist(self, path_file: str) -> bool:
        pass

    def check_extension_file(self, path_file: str, extension: str) -> bool:
        pass