import json
import requests
from faker import Faker

class SwaggerTestDataGenerator:
    def __init__(self, openapi_url):
        self.openapi_url = openapi_url
        self.fake = Faker()
        self.swagger_doc = self._fetch_openapi_data()
        self.components = self.swagger_doc.get("components", {}).get("schemas", {})

    def _fetch_openapi_data(self):
        """Fetch OpenAPI JSON from the given URL."""
        response = requests.get(self.openapi_url)
        response.raise_for_status()
        return response.json()

    def _generate_test_data(self, schema):
        """Recursively generate test data based on OpenAPI schema."""
        test_data = {}

        if "$ref" in schema:
            ref_path = schema["$ref"].split("/")[-1]
            return self._generate_test_data(self.components[ref_path])

        if "properties" in schema:
            for field, properties in schema["properties"].items():
                if "type" in properties:
                    if properties["type"] == "string":
                        test_data[field] = self.fake.word() if "password" not in field.lower() else self.fake.password()
                    elif properties["type"] == "integer":
                        test_data[field] = self.fake.random_int(min=1, max=1000)
                    elif properties["type"] == "number":
                        test_data[field] = round(self.fake.random_number(digits=5) / 100, 2)
                    elif properties["type"] == "boolean":
                        test_data[field] = self.fake.boolean()
                    elif properties["type"] == "array":
                        test_data[field] = [self._generate_test_data(properties["items"])]
                    elif properties["type"] == "object":
                        test_data[field] = self._generate_test_data(properties)

        return test_data

    def generate_test_data_for_all_endpoints(self):
        """Generate test data for all API endpoints with request bodies."""
        test_data_collection = {}
        
        for path, methods in self.swagger_doc["paths"].items():
            for method, details in methods.items():
                if "requestBody" in details:
                    schema = details["requestBody"]["content"]["application/json"]["schema"]
                    test_data = self._generate_test_data(schema)
                    test_data_collection[f"{path}"] = test_data

        return test_data_collection

 
# if __name__ == "__main__":
#     api_url = "http://localhost:8080/v3/api-docs"  # Set your API URL
#     generator = SwaggerTestDataGenerator(api_url)
    
#     test_data = generator.generate_test_data_for_all_endpoints()
    
#     for endpoint, data in test_data.items():
#         print(f"Test data for {endpoint}:\n", json.dumps(data, indent=2))
