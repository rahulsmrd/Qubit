import json

def deserializer(data):
    enrichedData = []
    locations_list = []
    similar_organizations_list = []
    affiliate_organizations_list = []
    company_name = data['companyName']
    company_url = data['url']
    company_id = data['companyId']
    locations = data['locations']
    enrichedData.append((company_name, company_url, company_id))
    # Handling location data
    for location in locations:
        location_tuple = (
            company_name, 
            location['country'],
            location['city'],
            location['postalCode'],
            location['headquarter']
        )
        locations_list.append(location_tuple)
    # Handling Similar organizations data
    similar_organizations = data.pop('similarOrganizations')
    for similar_organization in similar_organizations:
        similar_organization_tuple = (
            similar_organization['name'],
            similar_organization['url'],
            similar_organization['companyId'],
        )
        enrichedData.append(similar_organization_tuple)
        similar_organizations_list.append((company_name, similar_organization['name']))

    # Handling affiliated Organizations data
    affiliate_organizations1 = data.pop('affiliatedOrganizationsByEmployees')
    affiliate_organizations2 = data.pop('affiliatedOrganizationsByShowcases')
    for affiliated_organization1 in affiliate_organizations1:
        affiliated_organization_tuple1 = (
            affiliated_organization1['name'],
            affiliated_organization1['url'],
            affiliated_organization1['companyId'],
        )
        enrichedData.append(affiliated_organization_tuple1)
        affiliate_organizations_list.append((company_name, affiliated_organization1['name']))
    for affiliated_organization2 in affiliate_organizations2:
        affiliated_organization_tuple2 = (
            affiliated_organization2['name'],
            affiliated_organization2['url'],
            affiliated_organization2['companyId'],
        )
        enrichedData.append(affiliated_organization_tuple2)
        affiliate_organizations_list.append((company_name, affiliated_organization2['name']))
    return enrichedData, locations_list, similar_organizations_list, affiliate_organizations_list


def serializer(tabelName, data):
    non_duplicate_companies = set()
    non_duplicate_locations = set()
    non_duplicate_similar_organizations = set()
    non_dupllicate_affiliatedOrganizations = set()
    serialized_data = {
        "data": []
    }
    add_data = serialized_data['data']
    item_data = {}
    if tabelName == "EnrichedComapanyData":
        for item in data:
            if item[0] not in non_duplicate_companies:
                if len(item_data) != 0:
                    add_data.append(item_data)
                non_duplicate_companies.add(item[0])
                non_duplicate_locations.add(item[8])
                non_duplicate_similar_organizations.add(item[3])
                item_data = {
                    "companyName": item[0],
                    "url": item[1],
                    "companyId": item[2],
                    "locations": [
                        {
                            "country": item[6],
                            "city": item[7],
                            "postalCode": item[8],
                            "headquarter": item[9],
                        }
                    ],
                    "similarOrganizations": [
                        {
                            "companyName": item[3],
                            "url": item[4],
                            "companyId": item[5],
                        }
                    ],
                    "affiliatedOrganizations": [
                        {
                            "companyName": item[10],
                            "url": item[11],
                            "companyId": item[12],
                        }
                    ]
                }
            else:
                if item[3] not in non_duplicate_similar_organizations:
                    item_data['similarOrganizations'].append(
                        {
                            "companyName": item[3],
                            "url": item[4],
                            "companyId": item[5],
                        }
                    )
                    non_duplicate_similar_organizations.add(item[3])
                if item[8] not in non_duplicate_locations:
                    item_data['locations'].append(
                        {
                            "country": item[6],
                            "city": item[7],
                            "postalCode": item[8],
                            "headquarter": item[9],
                        }
                    )
                    non_duplicate_locations.add(item[8])
                if item[10] not in non_dupllicate_affiliatedOrganizations:
                    item_data['affiliatedOrganizations'].append(
                        {
                            "companyName": item[10],
                            "url": item[11],
                            "companyId": item[12],
                        }
                    )
                    non_dupllicate_affiliatedOrganizations.add(item[10])
    elif tabelName == 'similarOrganizations':
        for item in data:
            item_data = {
                "related_company": item[0],
                "similarOrganization_name": item[1]
            }
            add_data.append(item_data)
    elif tabelName == 'affiliatedOrganizations':
        for item in data:
            item_data = {
                "related_company": item[0],
                "affiliatedOrganization_name": item[1]
            }
            add_data.append(item_data)
    elif tabelName == 'locations':
        for item in data:
            item_data = {
                "companyName": item[1],
                "country": item[2],
                "city": item[3],
                "postalCode": item[4],
                "headquarter": item[5]
            }
            add_data.append(item_data)
    return json.dumps(serialized_data)