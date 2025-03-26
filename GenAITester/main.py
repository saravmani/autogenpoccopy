import os
from dotenv import load_dotenv
from modules.TestCasesSelfHealer import TestCasesSelfHealer
from modules.BDDSelfHealer import BDDSelfHealer
from modules.ModifiedBddFinder import ModifiedBddFinder
from modules.BDDValidator import BDDValidator
from modules.APITestCaseGenerator import APITestCaseGenerator
from modules.BDDGenerator import BddGenerator
from Tools.TestDataGeneratorTool import SwaggerTestDataGenerator
import json
load_dotenv()
 

def remove_code_blocks(text, lang): 
  text = text.replace("```"+lang, "")
  text = text.replace("```", "")
  text = text.replace("TERMINATE", "")
  return text.strip() 

# input("Hi I am Gen AI Tool . I can help you in generating automated BDD Features and PyTest test cases. Also i can Assist you in Self Healing the existing BDD Test cases and PyTest test cases. \n\n Press enter to continue...")

#Do you want to generat BDD and PyTest test cases for your API? Or Do you want 
user_input_choice = input("Select any below option to proceed :  \n 1. Generate BDD and PyTest test cases for your API \n 2. Generate PyTest test cases for existing BDD test cases \n 3. Self Heal your existing BDD and PyTest test cases \n ")


# api_base_url= input("Enter the Valid API Url :") ## "http://localhost:8080"
# api_swagger_url = input("Enter the Valid OpenAPI Url :") ## "http://localhost:8080"+"/v3/api-docs"

api_base_url=   "http://localhost:8080"
api_swagger_url =  "http://localhost:8080"+"/v3/api-docs"


print("Accessing Open API - to understand the API context and parameters")
generator = SwaggerTestDataGenerator(api_swagger_url)
test_data_dictionary = generator.generate_test_data_for_all_endpoints()



if user_input_choice=="1":
      


  ########################################################################


  for api_url, test_data in test_data_dictionary.items():
    print(f"Generating BDD for an API : {api_url}:\n")
    try:
      apiname = api_url.replace("/","_") 
      test_data=json.dumps(test_data_dictionary[api_url])

      # BddGenerator:
      bdd_generator = BddGenerator(api_url,test_data)
      task_statement = "Generate BDD Test cases in gherkin language, for the API with the given context, API parameters, API information. Api URL :  "+api_url
      answer = bdd_generator.generate_bdd_test_cases(task_statement)
      cleaned_text = remove_code_blocks(answer,"gherkin")
    
    except Exception as e:
              print(f"Error generating BDD test cases: {e}")


  print("**********************")
  ## GEN AI Helper for users to update the BDD test cases
  bdd_validator = BDDValidator()
  bdd_validator.update_bdd();
  
  print("**********************")
  user_input_choice = input("BDD Test cases are updated based on your inputs.. Enter 1 to generate the PyTest test cases for the BDD test cases")


  #######################################################################
if user_input_choice=="2":
  ## Generate the pytest test cases
  api_Test_Case_Generator = APITestCaseGenerator(api_base_url) 
  answer = api_Test_Case_Generator.generate_pytest_testcases(test_data_dictionary)
  print("Pytest cases generation completed .. ")
  print("**********************")



if user_input_choice=="3":
  ### Self Healing 
  modified_bddFinder = ModifiedBddFinder("","")
  bdd_files_needs_to_be_updated = modified_bddFinder.update_bbd_test_cases()
  # print(bdd_files_needs_to_be_updated)

  ## bdd_files_needs_to_be_updated = {'api_urls_with_content_modified': [{'url': '/api/users/register', 'content': 'The Phone number length should be 15. if this rule not passed then api should return 400.'}, {'url': '/api/users/login', 'content': 'Authenticates users by accepting email address. And Email address domain should be "gmail.com / yahoo.com" and password and generates a JWT token.'}]}
  BDD_self_healer = BDDSelfHealer()
  BDD_self_healer.heal_bdd_files(bdd_files_needs_to_be_updated)


  BDD_self_healer = TestCasesSelfHealer()
  BDD_self_healer.heal_test_files(bdd_files_needs_to_be_updated)

  print("**********************")

