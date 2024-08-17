create_table_query = """
            CREATE TABLE IF NOT EXISTS CompanyData (
                company_name VARCHAR(255) UNIQUE NOT NULL,
                company_linkedin_url VARCHAR(511) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS EnrichedComapanyData(
                company_name VARCHAR(255) UNIQUE NOT NULL,
                company_url VARCHAR(255) NOT NULL,
                company_id INT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS similarOrganizations (
                related_company_name VARCHAR(255),
                FOREIGN KEY (related_company_name) 
                REFERENCES EnrichedComapanyData(company_name),

                similar_organization_name VARCHAR(255),
                FOREIGN KEY (similar_organization_name) 
                REFERENCES EnrichedComapanyData(company_name)
            );
            CREATE TABLE IF NOT EXISTS affiliatedOrganizations (
                related_company_name VARCHAR(255),
                FOREIGN KEY (related_company_name) 
                REFERENCES EnrichedComapanyData(company_name),

                affiliatedOrganization_name VARCHAR(255),
                FOREIGN KEY (affiliatedOrganization_name) 
                REFERENCES EnrichedComapanyData(company_name)
            );
            CREATE TABLE IF NOT EXISTS EnrichedCompanyDataLocations(
                location_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255),
                FOREIGN KEY (company_name) 
                REFERENCES EnrichedComapanyData(company_name),

                location_country VARCHAR(255),
                location_city VARCHAR(255),
                location_pin VARCHAR(255) UNIQUE NOT NULL,
                location_headquarters BOOLEAN DEFAULT FALSE
            )
            """

insert_data_CompanyData = """
                INSERT INTO CompanyData (company_name, company_linkedin_url)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """

insert_data_EnrichedCompanyData = """
                INSERT INTO EnrichedComapanyData (
                company_name,
                company_url,
                company_id
                ) 
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
                """

insert_data_similarOrganizations = """
                INSERT INTO similarOrganizations (
                    related_company_name,
                    similar_organization_name
                )
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """

insert_data_affiliatedOrganizations = """
                INSERT INTO affiliatedOrganizations (
                    related_company_name,
                    affiliatedOrganization_name
                )
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """

insert_data_location = """
                INSERT INTO EnrichedCompanyDataLocations(
                    company_name,
                    location_country,
                    location_city,
                    location_pin,
                    location_headquarters
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """

show_enrichedCompanyData_table = """
                SELECT 
                    ecd.company_name,
                    ecd.company_url,
                    ecd.company_id,
                    so_data.company_name,
                    so_data.company_url,
                    so_data.company_id,
                    lo_data.location_country,
                    lo_data.location_city,
                    lo_data.location_pin,
                    lo_data.location_headquarters,
                    afo_data.company_name,
                    afo_data.company_url,
                    afo_data.company_id
                FROM
                    EnrichedComapanyData AS ecd
                LEFT JOIN
                    (
                        SELECT 
                            so.related_company_name,
                            ecd2.company_name,
                            ecd2.company_url,
                            ecd2.company_id
                        FROM
                            similarOrganizations AS so
                        LEFT JOIN
                            EnrichedComapanyData AS ecd2
                        ON so.similar_organization_name = ecd2.company_name
                    ) AS so_data
                    ON ecd.company_name = so_data.related_company_name
                LEFT JOIN
                    (
                        SELECT
                            af.related_company_name,
                            ecd3.company_name,
                            ecd3.company_url,
                            ecd3.company_id
                        FROM
                            affiliatedOrganizations AS af
                        LEFT JOIN
                            EnrichedComapanyData AS ecd3
                        ON af.affiliatedOrganization_name = ecd3.company_name
                    ) AS afo_data
                    ON ecd.company_name = afo_data.related_company_name
                LEFT JOIN
                    EnrichedCompanyDataLocations AS lo_data
                    ON ecd.company_name = lo_data.company_name
                ORDER BY 
                    ecd.company_name;
                """