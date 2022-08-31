import pytest
import exam_tester.io

'''
    Verifies all the subclasses inside io.py
'''

# Section to create all the fixtures to mock all the test 

#@pytest.fixture()

    # Create a pandas that mocks a file with new questions but doesn't have 4 columns
    # Create a pandas that mocks a file with existing questions but have less than 5 columns

    # Create an empty pandas

    # Create a pandas that mocks a file with new questions but doesn't the 1 column doesn't have the module
    # Create a pandas that mocks a file with existing questions but the 2 column doesn't have the module

    # Create a pandas that mocks a file with new questions but the last column doesn't use the separator (##) to indicate each column
    # Create a pandas that mocks a file with existing questions but the last column doesn't use the separator (##) to indicate each column

    # Create a pandas that mocks a file with existing questions but the ID are messed up
    
    # Create a pandas that mocks a correct file with new questions
    # Create a pandas that mocks a correct file with existing questions

# Test the module used to import new questions to the system and existing questions

    # Trying to import and the file doesn't exists

    # Trying to import and the file doesn't have the correct extension (!=csv)

    # The file is imported but is empty

    # FIXTURE OF X COLUMNS (new !=4)(existing >5)
    # The file is imported but doesn't enough columns

    # FIXTURE TO KNOW THE CORRECT COLUMN (new == 1)(existing == 2)

    # The file is imported but the wrong answers doesn't use the separator (##)

    # Exclusive for importing existing questions    

        # The file is imported but one ID of the questions doesn't have a valid code

    # Trying to import a correct pandas as new and existing questions

# Test log_results

    # Trying to create the file for the first time

    # Appending new data to the file where all the history is saved

# Test save_questions

    # Trying to save a question that already exist by question and module

    # Trying to add new questions to the curred existing file

    # Trying to create for the first time the file where all the questions are gonna get saved