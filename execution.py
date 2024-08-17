from getAPIdata import get_data_from_api
from DatabaseQueries import DatabaseManager
from serializers import serializer, deserializer

object = DatabaseManager()

# values = [('ERCOT', 'https://www.linkedin.com/company/ercot'), ('NRG Energy', 'https://www.linkedin.com/company/nrgenergy')]
# object.insert('CompanyData', values)

def create_payload(data):
    non_duplicate_company_data = set()
    payload = {"links": []}
    for item in data:
        if item[0] not in non_duplicate_company_data:
            payload['links'].append(item[1])
    return payload

company_data = object.showTabel('CompanyData')
payload = create_payload(company_data)
data = get_data_from_api(payload)

for item in data.pop('data'):
    enrichedData, locations_list, similar_organizations_list, affiliate_organizations_list = deserializer(item.pop('data'))
    object.insert('EnrichedCompanyData', enrichedData)
    object.insert('similarOrganizations', similar_organizations_list)
    object.insert('location', locations_list)
    object.insert('affiliatedOrganizations', affiliate_organizations_list)

table_data = object.showTabel("EnrichedComapanyData")

object.close()

json_data = serializer('EnrichedComapanyData', table_data)

print(json_data)

# with open('Output_test.json', 'w') as outfile:
#     json.dump(json_data, outfile, indent=4)


# object.delete_table('CompanyData')
# object.delete_table('EnrichedComapanyData')
# object.delete_table('similarOrganizations')
# object.delete_table('affiliatedOrganizations')
# object.delete_table('EnrichedCompanyDataLocations')