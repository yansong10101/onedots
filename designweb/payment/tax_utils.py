__author__ = 'zys'
import csv
from django.core.cache import cache
from time import sleep
from designweb.payment import *


TAX_FILE_PATH = '/Users/zys/Downloads/ca_tax_2015.csv'
TAX_COLUMN_FIELD_STATE = 'state'
TAX_COLUMN_FIELD_ZIP = 'zip'
TAX_COLUMN_FIELD_REGION_NAME = 'region_name'
TAX_COLUMN_FIELD_REGION_CODE = 'region_code'
TAX_COLUMN_FIELD_COMBINE_RATE = 'combine_rate'
TAX_COLUMN_FIELD_STATE_RATE = 'state_rate'
TAX_COLUMN_FIELD_COUNTY_RATE = 'county_rate'
TAX_COLUMN_FIELD_CITY_RATE = 'city_rate'
TAX_COLUMN_FIELD_SPECIAL_RATE = 'special_rate'


def save_tax_to_cache(key, value):
    cache.set(key, value, timeout=0)
    sleep(0.0005)


def get_tax_combine_rate_by_zip(key_zip):
    tax_dict = cache.get(key_zip)
    return tax_dict[TAX_COLUMN_FIELD_COMBINE_RATE] or 0.00


def read_tax_csv_to_dict(input_file):
    with open(input_file, 'rU') as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        next(reader)
        for row in reader:
            row_list = str.split(row[0], ',')
            key_zip_code = row_list[1]
            values = {
                TAX_COLUMN_FIELD_STATE: row_list[0],
                TAX_COLUMN_FIELD_ZIP: row_list[1],
                TAX_COLUMN_FIELD_REGION_NAME: row_list[2],
                TAX_COLUMN_FIELD_REGION_CODE: row_list[3],
                TAX_COLUMN_FIELD_COMBINE_RATE: row_list[4],
                TAX_COLUMN_FIELD_STATE_RATE: row_list[5],
                TAX_COLUMN_FIELD_COUNTY_RATE: row_list[6],
                TAX_COLUMN_FIELD_CITY_RATE: row_list[7],
                TAX_COLUMN_FIELD_SPECIAL_RATE: row_list[8],
            }
            save_tax_to_cache(key_zip_code, values)
            print(get_tax_combine_rate_by_zip(key_zip_code))


def get_tax_combine_rate_by_zip_from_iron_cache(key_zip):
    tax_cache = IronCache(project_id=IRON_CACHE_PROJECT_ID, token=IRON_CACHE_TOKEN)
    item = tax_cache.get(str(key_zip), cache=IRON_CACHE_TAX_BUCKET)
    tax_dict = json.loads(item.value)
    if not tax_dict:
        return 0.00
    return tax_dict[TAX_COLUMN_FIELD_COMBINE_RATE]
