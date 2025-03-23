from Tools.TestDataGeneratorTool import SwaggerTestDataGenerator
import json

# Initialize the generator with the OpenAPI URL
api_url = "http://localhost:8080/v3/api-docs"
generator = SwaggerTestDataGenerator(api_url)

# Generate test data for all endpoints
test_data = generator.generate_test_data_for_all_endpoints()

# Print the generated test data
for endpoint, data in test_data.items():
    print(f"Test data for {endpoint}:\n", json.dumps(data, indent=2))
