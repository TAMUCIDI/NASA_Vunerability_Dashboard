import os

cwd = os.path.dirname(os.path.realpath(__file__))
# Census Tract Shapefile Path
shapefile_path = cwd + "/data/census_tract/tl_2020_40_tract.shp"

#census data Excel Path
census_data_path = cwd + "/data/census_data/data.xlsx"

AREA_CHOICES = (
    ('SFA', 'SFA'),
    ('BGA', 'BGA'),
    ('ERA', 'ERA'),
    ('BDA', 'BDA'),
    ('SBA', 'SBA'),
    ('MNA', 'MNA'),
    ('MRA', 'MRA'),
    ('LAA', 'LAA'),
    ('CCA', 'CCA'),
    ('SDA', 'SDA'),
    ('ALL', 'ALL'),
)

YEAR_RANGE = [
    '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020', '2021'
]

NORMALIZE_COLUMNS = [
    'Speed_90', 
    'Mili_Dist', 
    'Shoreline_Dist', 
    'NEAR_DIST_PROT',
    '2019',
    '2020',
    '2021',
]