import requests
from requests.exceptions import HTTPError
import re

def hlab_results(url):
    try:
        r = requests.get(url)
        if r.json():
            return r.json()
        else:
            print("No results found")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

def check_collection(x):
    # can skip hardcode by running list_collection, but time tradeoff?
    if x in ['frus', 'clinton', 'pdb', 'cfpf', 'kissinger', 'nato']:   # I based this off list_collection results, but in R more options?
        return x
    else:
        raise Exception("Collection not found in History Lab database")
        
def check_entity_type(x):
    if isinstance(x, list) == False:
        if x in ['country', 'person', 'topic']:
            return x
        else:
            raise Exception("Only acceptable entity types are 'country', 'person', and 'topic'")
    else:
        for i in x:
            if i in ['country', 'person', 'topic']:
                continue
            else:
                raise Exception("Only acceptable entity types are 'country', 'person', and 'topic'")
        return x
        
def check_date(date):
    if date:
        check = re.search(r'^\d{4}-\d{2}-\d{2}$', date)
        if check:
            if int(date[5:7]) > 12:
                raise Exception("Please enter a valid date with the format 'YYYY-MM-DD'")
        else:
            raise Exception("Please enter a valid date with the format 'YYYY-MM-DD'")
        
def check_date_range(start, end):
    if start and end:
        if int(end[0:4]) < int(start[0:4]):
            raise Exception("End date must be later than start date")
        elif (int(end[0:4]) == int(start[0:4])) and (int(end[5:7]) < int(start[5:7])):
            raise Exception("End date must be later than start date")
        elif (int(end[5:7]) == int(start[5:7])) and (int(end[0:4]) < int(start[0:4])) and (int(end[8:10]) < int(start[8:10])):
            raise Exception("End date must be later than start date")
        else:
            pass
    elif start and not(end):
        raise Exception("Please provide an end date")
    elif not(start) and end:
        raise Exception("Please provide a start date")
        
def convert_to_list(x):
    if isinstance(x, list) == False:
        temp = []
        if "," in x:
            comma_split = re.split(",", x)
            for i in comma_split:
                temp.append(i.strip())
        else:
            temp.append(x)
        return temp
    else:
        return x
    
def check_fields(x):
    if x:
        if isinstance(x, list) == False:
            if x not in ["authored","body","body_html","body_summary","chapt_title","countries","collection","date","date_year","date_month",
                     "from_field","doc_id","location","nuclear","persons","topics","classification","refs","cable_references","source","source_path",
                     "cable_type","subject","title","to_field","tags","description","category","pdf","title_docview","orighand","concepts",
                     "type","office","readability","persons","countries","person_ids"]:
                raise Exception(f"Field Error: '{x}' not a valid field")
        else:
            invalids = []
            for i in x:
                if i in ["authored","body","body_html","body_summary","chapt_title","countries","collection","date","date_year","date_month",
                         "from_field","doc_id","location","nuclear","persons","topics","classification","refs","cable_references","source","source_path",
                         "cable_type","subject","title","to_field","tags","description","category","pdf","title_docview","orighand","concepts",
                         "type","office","readability","persons","countries","person_ids"]:
                    continue
                else:
                    invalids.append(i)
            if invalids:
                invalid_str = ''
                count = 0
                for i in invalids:
                    if count == 0:
                        invalid_str = invalid_str + i
                    else:
                        invalid_str = invalid_str + ", " + i
                    count = count + 1
                raise Exception(f"'{invalid_str}' is/are not valid field(s)")

def config_search(search, join_or):
    if join_or == False:
        join = 'and=('
    else:
        join = 'or=('
    url = join
    for i in range(0, len(search)):
        strip = search[i].strip()
        subbed = re.sub(" ", "%20", strip)
        if i%2 == 0:
            temp = f"full_text.phfts.{subbed},"
        else:
            temp = f"full_text.wfts.{subbed},"
        url = url + temp
    url = url[:len(url)-1] + ')'
    return url

def config_ent(entity_value):
    url = ''
    for i in range(0, len(entity_value)):
        strip = entity_value[i].strip()
        subbed = re.sub(" ", "%20", strip)
        url = url + subbed + ','
    url = url[:len(url)-1]
    return url

def check_bool(param):
    assert param == False or param == True, f"Value of parameter '{param}' must be True or False"
    
def entity_url_creator(ent_value, ent_or):
    if ent_or == False:
        join = 'cs'
    else:
        join = 'ov'
    ent_url = join + '.{' + config_ent(ent_value) + '}'
    return ent_url