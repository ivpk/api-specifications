# Lithuania API Specifications

This project provides OpenAPI specifications for Lithuania's government APIs. OpenAPI is a specification for building
APIs that enables developers to design, document, and test their APIs.

## Adding New OpenAPI Specifications

To add a new OpenAPI specification, follow these steps:

1. Open [`specifications.json`](specifications.json) file.
2. Add a new organization with their specifications in the following format:

   ```yaml
   {
     "id": "<organization_id>",
     "label": "<organization_name>",
     "specifications": [
       {
         "id": "<specification_id>",
         "label": "<specification_name>",
         "url": "<specification_url>"
       }
     ]
   }
   ```

   Replace `<organization_id>`, `<organization_name>`, `<specification_id>`, `<specification_name>`,
   and `<specification_url>` with the appropriate values for your new OpenAPI specification.

3. Save the file.

Your new OpenAPI specification will be automatically synced to the [`openapi`](openapi) directory and will appear
at https://api.gov.lt/.

## Viewing OpenAPI Specifications

You can view OpenAPI specifications using tools such as the  [Swagger Editor](https://editor.swagger.io/).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Technical Details

The specifications are synced to the [`openapi`](openapi) directory using [openapi.py](scripts/openapi/openapi.py). This
function downloads the specification, formats it, and saves it as a
JSON file with a name that includes the organization and specification IDs. If any errors occur during this process, a
warning is logged.