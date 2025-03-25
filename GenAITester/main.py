import os
from dotenv import load_dotenv
from modules.ModifiedBddFinder import ModifiedBddFinder
from modules.BDDValidator import BDDValidator
from modules.APITestCaseGenerator import APITestCaseGenerator
from modules.BDDGenerator import BddGenerator
from Tools.TestDataGeneratorTool import SwaggerTestDataGenerator
from utils.fileutils import save_text_to_file
import json

load_dotenv()
# Initialize the generator with the OpenAPI URL
api_base_url="http://localhost:8080"
api_swagger_url = api_base_url+"/v3/api-docs"
# generator = SwaggerTestDataGenerator(api_swagger_url)
# test_data_dictionary = generator.generate_test_data_for_all_endpoints()



def remove_code_blocks(text, lang): 
  text = text.replace("```"+lang, "")
  text = text.replace("```", "")
  text = text.replace("TERMINATE", "")
  return text.strip() 



# #######################################################################


# for api_url, test_data in test_data_dictionary.items():
#   print(f"Generating BDD for and API : {api_url}:\n")
#   try:
#     # api_url="/api/users/register"
#     apiname = api_url.replace("/","_") 
#     test_data=json.dumps(test_data_dictionary[api_url])

#     # BddGenerator:
#     bdd_generator = BddGenerator(api_url,test_data)
#     task_statement = "Generate BDD Test cases in gherkin language, for the API with the given context, API parameters, API information. Api URL :  "+api_url
#     answer = bdd_generator.generate_bdd_test_cases(task_statement)
#     # cleaned_text = remove_code_blocks(answer,"gherkin")

#     # full_bdd_file_path = os.path.join(os.getenv('BDDFILESPATH'), apiname+".feature")
#     # save_text_to_file(cleaned_text, full_bdd_file_path) 
#   except Exception as e:
#             print(f"Error generating BDD test cases: {e}")


# print("**********************")
# print("BDD Test cases are generated. You can validate the Feature files. If you want to update BDD Validator agent will hep you to update the test cases")
# input("Press ENTER to proceed...")

# bdd_validator = BDDValidator()
# bdd_validator.update_bdd();
 
# print("**********************")
# print("BDD Test cases are updated based on your inputs")


# #######################################################################

# ## Generate the pytest test cases
# api_Test_Case_Generator = APITestCaseGenerator(api_base_url) 
# answer = api_Test_Case_Generator.generate_pytest_testcases(test_data_dictionary)
 
# print("**********************")





modified_bddFinder = ModifiedBddFinder("","")
bdd_files_needs_to_be_updated = modified_bddFinder.update_bbd_test_cases()
print(bdd_files_needs_to_be_updated)
 

# for bdd_modificatioon_context in bdd_files_needs_to_be_updated.items():
