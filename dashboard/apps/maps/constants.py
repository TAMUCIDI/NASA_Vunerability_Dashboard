import os

cwd = os.path.dirname(os.path.realpath(__file__))
# Census Tract Shapefile Path
shapefile_path = cwd + "/data/census_tract/tl_2020_40_tract.shp"

#census data Excel Path
census_data_path = cwd + "/data/census_data/data.xlsx"

#census data new CSV Path
census_data_new = cwd + "/data/census_data_new/merged_file_2020.csv"

criterion_list = [
    'max', # Female Percent
    'max', # Age Percent
    'max', # Property Percent
    'max', # No Diploma Percent
    'max', # Living Alone Percent
    'max', # Minority Percent
    'max', # Unemployment Percent
    'max', # Language Percent
    'max', # Rent Percent
    'max', # No Vehicle Percent
    'max', # No Insurance Percent
    'max', # Disability Percent
    'min', # Computer Percent
    'max', # No Internet Percent
    'max', # No Phone Percent
]

COUNTY_LIST = ['017', '027', '087', '051', '109', '125']

COLUMNS = [
            'geometry',
            'GEOID',
            'Female%',
            'Age<5>65%',
            '>15property%',
            'nodiploma%',
            '%livingalone',
            '%minority',
            '%unemployment',
            '%language',
            '%renthouse',
            'Novehicle%',
            '%noinsurance',
            '%disability',
            '%computer',
            '%nointernet',
            '%nophone',  ]

COLUMNS_NEW = [
    'geometry',
    'GEOID',
    'Female.',
    'Age.5.65.', 
    'X.15property.', 
    'nodiploma.', 
    'X.livingalone',
    'X.minority', 
    'X.unemployment', 
    'X.language', 
    'X.renthouse',
    'Novehicle.', 
    'X.noinsurance', 
    'X.disability', 
    'X.computer',
    'X.nointernet', 
    'X.nophone'
]

COLUMNS_RENAME_DICT = {
                    'Female%': 'Female_Percent',
                    'Age<5>65%': 'Elder&Young_Percent',
                    '>15property%': 'LowIncome_Percent',
                    'nodiploma%': 'Low_Educ_Percent',
                    '%livingalone': 'Living_Alone_Percent',
                    '%minority': 'Minority_Percent',
                    '%unemployment': 'Unemployment_Percent',
                    '%language': 'Language_Percent',
                    '%renthouse': 'RentHouse_Percent',
                    'Novehicle%': 'No_Vehicle_Percent',
                    '%noinsurance': 'No_Insurance_Percent',
                    '%disability': 'Disable_Percent',
                    '%computer': 'Computer_Availability',
                    '%nointernet': 'No_Internet_Percent',
                    '%nophone': 'No_Phone_Percent'
                }

COLUMNS_NEW_RENAME_DICT = {
    'Female.': 'Female_Percent',
    'Age.5.65.': 'Elder&Young_Percent',
    'X.15property.': 'LowIncome_Percent',
    'nodiploma.': 'Low_Educ_Percent',
    'X.livingalone': 'Living_Alone_Percent',
    'X.minority': 'Minority_Percent',
    'X.unemployment': 'Unemployment_Percent',
    'X.language': 'Language_Percent',
    'X.renthouse': 'RentHouse_Percent',
    'Novehicle.': 'No_Vehicle_Percent',
    'X.noinsurance': 'No_Insurance_Percent',
    'X.disability': 'Disable_Percent',
    'X.computer': 'Computer_Availability',
    'X.nointernet': 'No_Internet_Percent',
    'X.nophone': 'No_Phone_Percent'
}