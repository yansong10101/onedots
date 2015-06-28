__author__ = 'zys'
from django.core.management.base import BaseCommand
from designweb.payment.tax_utils import *


class Command(BaseCommand):
    args = '< email_address email_address ...>'
    help = 'please enter email addresses'

    def handle(self, *args, **options):

        tax_cache = IronCache(project_id=IRON_CACHE_PROJECT_ID, token=IRON_CACHE_TOKEN)
        with open(TAX_FILE_PATH, 'rU') as f:
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
                tax_cache.put(cache=IRON_CACHE_TAX_BUCKET, key=key_zip_code, value=values)
                sleep(0.0005)
                print(key_zip_code)
