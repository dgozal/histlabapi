import requests
from requests.exceptions import HTTPError
import re


#################################################################################################
####################################### Utility Functions #######################################
#################################################################################################

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



################################################################################################
######################################## Main Functions ########################################
################################################################################################

def list_collections():
    """
    Lists the various document collections that are available in the History Lab's database.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    A JSON object listing all the various document collections and the number of documents in each collection
    
    Example
    -------
    >>> from histlabapi import histlabapi as hl
    >>> hl.list_collections()
    [{'corpus': 'frus', 'doc_cnt': 209046},
     {'corpus': 'cia', 'doc_cnt': 935716},
     {'corpus': 'clinton', 'doc_cnt': 54149},
     {'corpus': 'pdb', 'doc_cnt': 5011},
     {'corpus': 'cfpf', 'doc_cnt': 3214293},
     {'corpus': 'kissinger', 'doc_cnt': 4552},
     {'corpus': 'nato', 'doc_cnt': 46002}]
    """
    return hlab_results("http://api.foiarchive.org/corpora")


def hlab_overview(collection = None, sort = None, entity_type = None, start_date = None, end_date = None, limit = 25, run = False):   
    """
    Provides an overview of the History Lab's contents by listing all the entities of a certain type that appear in the History Lab's
    collection of texts. Users can also filter this search by a date range.
    
    Parameters
    ----------
    collection: String
        A string that can be used to filter results to a specific document collection (eg. 'frus').
    sort: None, 'asc' or 'desc'
        A string specifying how you want your results sorted. If a None object is given, results will not be sorted.
    entity_type: 'person', 'topic' or 'country'
        A string specifying the type of entities you want the function to display. 
    start_date: String (in the YYYY-MM-DD format)
        A string specifying the start of the date range of the documents from which the specified entity types will be displayed. 
        Need to provide an end date as well if using this.
    end_date: String (in the YYYY-MM-DD format)
        A string specifying the end of the date range of the documents from which the specified entity types will be displayed. 
        Need to provide a start date as well if using this.
    limit: Integer
        An integer specifying the maximum number of entities this function will display. The default limit is 25.
    run: Bool
        If False, function will only return the API URL. If True, function will return the JSON object that is generated 
        by the full API query.
        
    Returns
    -------
    Either a string specifying the URL that is needed to query the desired results from the API, or a JSON object containing the 
    list of all the entities of the specified type that appear in the collection specified within the specified date range.
    
    Example
    -------
    >>> from histlabapi import histlabapi as hl
    >>> hl.hlab_overview(collection = 'frus', sort = None, entity_type = 'person', limit = 5, run = False)
    'http://api.foiarchive.org/entities?entity_type=eq.person&corpus=eq.frus&limit=5'
    >>> hl.hlab_overview(collection = 'frus', sort = None, entity_type = 'person', limit = 5, run = True)
    [{'entity_type': 'person',
      'entity_id': '100001',
      'entity_name': 'Aaron, David Laurence',
      'corpus': 'frus',
      'ref_cnt': 155},
     {'entity_type': 'person',
      'entity_id': '100004',
      'entity_name': 'Abbas, Ferhat',
      'corpus': 'frus',
      'ref_cnt': 5},
     {'entity_type': 'person',
      'entity_id': '100007',
      'entity_name': 'Abbas Hilmi Pasha',
      'corpus': 'frus',
      'ref_cnt': 1},
     {'entity_type': 'person',
      'entity_id': '100009',
      'entity_name': 'Abbey, Glenn A.',
      'corpus': 'frus',
      'ref_cnt': 2},
     {'entity_type': 'person',
      'entity_id': '100010',
      'entity_name': 'Abbott, Douglas C.',
      'corpus': 'frus',
      'ref_cnt': 2}]
    """
    # Checks
    check_bool(run)
    assert isinstance(limit, int) == True, "Value of parameter 'limit' must be an integer"
    if sort != None and sort != 'asc' and sort != 'desc':
        print("Value of parameter 'sort' must be blank, 'asc' or 'desc'. Defaulting to no sort")
        sort = None
    check_entity_type(entity_type)
    check_date(start_date)
    check_date(end_date)
    check_date_range(start_date, end_date)
    # Create URL
    url = 'http://api.foiarchive.org/entities?entity_type=eq.' + entity_type
    if sort:
        url = url + '&order=ref_cnt.' + sort
    if collection:
        check_collection(collection)
        url = url + '&corpus=eq.' + collection
    if start_date and end_date:
        url = url + '&authored=gte.' + start_date + '&authored=lte.' + end_date
    url = url + '&limit=' + str(limit)
    if run == False:
        return(url)
    else:
        return hlab_results(url)

    
def hlab_search(text, fields = None, join_or = False, start_date = None, end_date = None, collection = None, limit = 25, run = False):
    """
    A search function that allows users to find documents that have the specified search terms in their texts.
    
    Parameters
    ----------
    text: String or list
        The search term that the user wants to look up. Can be input as a list if the user wishes to have multiple search terms.
    fields: String or list
        Series of fields that the user wants to display for each document that the search function finds. 
        Can be input as a list if the user wishes to have multiple fields displayed. If no field is provided, 
        the function defaults to displaying the doc_id, authored, and title fields.
    join_or: Bool
        If True, the search terms will be joined by an OR connector. If False, the search terms will be joined by an AND connector. 
        To illustrate, if the user inputs ['A', 'B'] in the text parameter and True in the join_or parameter, this function will 
        return all the documents that contain either 'A' or 'B'.
    start_date: String (in the YYYY-MM-DD format)
        A string specifying the start of the date range of the documents which this function will search for. 
        Need to provide an end date as well if using this.
    end_date: String (in the YYYY-MM-DD format)
        A string specifying the end of the date range of the documents which this function will search for. 
        Need to provide a start date as well if using this.
    collection: String
        A string that can be used to filter results to a specific document collection (eg. 'frus').
    limit: Integer
        An integer specifying the maximum number of documents this function will display. The default limit is 25.
    run: Bool
        If False, function will only return the API URL. If True, function will return the JSON object that is 
        generated by the full API query.
        
    Returns
    -------
    Either a string specifying the URL that is needed to query the desired results from the API, or a JSON object containing 
    the list of all the documents - along with the specified fields - that match the search query that the function generates.
    
    Example
    -------
    >>> from histlabapi import histlabapi as hl
    >>> hl.hlab_search('league of nations', run = False)
    'http://api.foiarchive.org/documents?and=(full_text.phfts.league%20of%20nations)&select=doc_id,authored,title&limit=25'
    >>> hl.hlab_search(['league of nations', 'trade'], fields = ['doc_id', 'title', 'countries'], join_or = True, limit = 5, run = True)
    [{'doc_id': '0000BA89',
      'title': 'TELECON WITH DAVID BINDER AT 3:21 P.M.',
      'countries': ['Argentina', 'Denmark', 'Soviet Union']},
     {'doc_id': '0000BB01',
      'title': 'TELECON WITH SONNENFELDT AT 8:10 P.M.',
      'countries': ['Soviet Union']},
     {'doc_id': '0000BB02',
      'title': 'TELECON WITH WILLIAM ROGERS AT 8:21 P.M.',
      'countries': ['Ecuador']},
     {'doc_id': '0000BB08',
      'title': 'TELECON WITH BERNIE GWERTZMAN AT 3:12 P.M.',
      'countries': ['Cambodia',
       'Chile',
       'Egypt',
       'Israel',
       'Japan',
       'Soviet Union',
       'Turkey',
       'United States',
       'Vietnam']},
     {'doc_id': '0000BB0A',
      'title': 'TELECON WITH SONNENFELDT AT 2:34',
      'countries': None}]
    """
    # Checks
    check_bool(run)
    check_bool(join_or)
    assert isinstance(limit, int) == True, "Value of parameter 'limit' must be an integer"
    check_fields(fields)
    check_date(start_date)
    check_date(end_date)
    check_date_range(start_date, end_date)
    # Create URL
    url = "http://api.foiarchive.org/documents?"
    text = convert_to_list(text)
    search = config_search(text, join_or)
    url = url + search + "&select="
    if not fields:
        fields = ['doc_id', 'authored', 'title']
    else:
        fields = convert_to_list(fields)
    for i in fields:
        url = url + i + ","
    url = url[:len(url)-1] 
    if collection:
        check_collection(collection)
        url = url + '&corpus=eq.' + collection
    if start_date and end_date:
        url = url + '&authored=gte.' + start_date + '&authored=lte.' + end_date
    url = url + '&limit=' + str(limit)
    if run == False:
        return(url)
    else:
        return hlab_results(url)
    
    
def find_entity_id(entity_type, value = None):
    """
    Allows users to find the IDs of the entities that they are looking for
    
    Parameters
    ----------
    entity_type: 'country', 'topic', or 'person'
        The type of entity users want to search for
    value: String
        The actual entity the user wants to search for
    
    Returns
    -------
    A JSON object listing the names and IDs of all the entities that match the user's search term. An important thing to note is that 
    the same entity can have different IDs if they appear in multiple collections. For example, Richard Nixon has three different IDs 
    here: '190882', 'hrc5593', 'kiss190882'. Each ID corresponds to the version of Richard Nixon that appears in each different collection 
    of documents. So '190882' refers to all the instances of Richard Nixon that appear in the FRUS documents, 'hrc5593' to the instances 
    that appear in the Hillary Clinton emails, and 'kiss190882' to those that appear in the Kissinger phone calls.
    
    Examples
    --------
    >>> from histlabapi import histlabapi as hl
    >>> hl.find_entity_id('person', 'Nixon')
    [{'full_name': 'Nixon, Patricia', 'person_id': '109881'},
     {'full_name': 'Nixon, Richard M.', 'person_id': '109882'},
     {'full_name': 'Nixon, Robert', 'person_id': '109883'},
     {'full_name': 'Nixon, Patricia', 'person_id': 'hrc5592'},
     {'full_name': 'Nixon, Richard; Nixon, Richard M.; Nixon, Richard Milhouse',
      'person_id': 'hrc5593'},
     {'full_name': 'Cox, Tricia Nixon', 'person_id': 'hrc10032'},
     {'full_name': 'Cox, Tricia Nixon', 'person_id': 'kiss10032'},
     {'full_name': 'Nixon, Richard; Nixon, Richard M.; Nixon, Richard Milhouse',
      'person_id': 'kiss109882'}]
    >>> hl.find_entity_id('country', 'Indonesia')
    [{'country_name': 'Indonesia', 'country_id': '360'}]
    """
    if not entity_type:
        raise Exception("Please supply an entity: country, topic, and/or person")
    check_entity_type(entity_type)
    if not value:
        raise Exception("Please supply a value for the entity")
    if entity_type == 'country':
        search = "countries?country_name=ilike.*" + value + "*&select=country_name,country_id"
    elif entity_type == 'topic':
        search = "topics?topic_name=ilike.*" + value + "*&select=topic_name,topic_id"
    elif entity_type == 'person':
        search = "persons?full_name=ilike.*" + value + "*&select=full_name,person_id"
    url = "http://api.foiarchive.org/" + search
    return hlab_results(url)


def hlab_entity(country = None, topic = None, person = None, country_or = False, topic_or = False, person_or = False, fields = None, 
                collection = None, date = None, start_date = None, end_date = None, summary = False, limit = 25, run = False):
    """
    A search function that allows users to look for documents that contain the entities that they are looking for
    
    Parameters
    ----------
    country: String or list
        Specifies the countries that the user wants to use to search documents with. Can be input as a list if the user wishes to search for
        multiple countries.
    topic: String or list
        Specifies the topics that the user wants to use to search documents with. Can be input as a list if the user wishes to search for
        multiple topics.
    person: String or list
        Specifies the persons that the user wants to use to search documents with. Can be input as a list if the user wishes to 
        search for multiple persons. Since search terms can return multiple results (eg. there are more than one "Kennedy"s), 
        users will need to input the specific person ID in this parameter. These IDs can be retrieved using the 
        find_entity_id function.
    country_or: Bool
        If True, joins the countries users are using as their search entities with an OR connector. If False, joins them 
        with an AND connector. To illustrate, if the user provides ['A', 'B'] in the parameter country and True in the country_or 
        parameter, the function will return documents that contain either the country 'A' or 'B'.
    topic_or: Bool
        Same like above but for topics.
    person_or: Bool
        Same like above but for persons.
    fields: String or list
        Series of fields that the user wants to display for each document that the search function finds. Can be input
        as a list if the user wishes to have multiple fields displayed. If no field is provided, the function defaults 
        to displaying the doc_id, authored, and title fields.
    collection: String    
        A string that can be used to filter results to a specific document collection (eg. 'frus').
    date: String (in the YYYY-MM-DD format)
        A string specfying the exact date of the documents this function will search for. 
        Mutually exclusive with the start_date and end_date parameters.
    start_date: String (in the YYYY-MM-DD format)
        A string specifying the start of the date range of the documents which this function will search for. 
        Need to provide an end date as well if using this.
    end_date: String (in the YYYY-MM-DD format)
        A string specifying the end of the date range of the documents which this function will search for. 
        Need to provide a start date as well if using this.
    summary: Bool
        If True, result is a summary that count the number of documents that contain the specific entity searched for. 
        When using summary, can only search for one entity at a time. Date filters also do not work.
    limit: Integer
        An integer specifying the maximum number of documents this function will display. The default limit is 25.
    run: Bool
        If False, function will only return the API URL. If True, function will return the JSON object that is 
        generated by the full API query.
    
    Returns
    -------
    Either a string specifying the URL that is needed to query the desired results from the API, or a JSON object containing the 
    list of all the documents - along with the specified fields - that match the search query that the function generates.
    
    Examples
    --------
    >>> from histlabapi import histlabapi as hl
    >>> hl.hlab_entity(collection = 'frus', country = 'Belize', run = False, limit = 5)
    'http://api.foiarchive.org/documents?countries=cs.{Belize}&select=doc_id,authored,title&corpus=eq.frus&limit=5'
    >>> hl.hlab_entity(collection = 'frus', country = 'Belize', run = True, limit = 5)
    [{'doc_id': 'frus1865p4d471',
      'authored': '1865-04-28T00:00:00+00:00',
      'title': 'British Honduras Company'},
     {'doc_id': 'frus1914Suppd474',
      'authored': '1914-09-03T19:00:00+00:00',
      'title': '\nThe Consul General at London (\nSkinner\n) to the Secretary of\n                                        State\n\n'},
     {'doc_id': 'frus1914Suppd849',
      'authored': '1914-12-18T00:00:00+00:00',
      'title': '\nThe Ambassador in Great Britain (\nPage\n) to the Secretary of\n                                    State\n\n'},
     {'doc_id': 'frus1915Suppd1257',
      'authored': '1915-03-26T00:00:00+00:00',
      'title': '\nThe British Ambassador (\nSpring Rice\n) to the\n\nSecretary of State\n\n'},
     {'doc_id': 'frus1915Suppd1263',
      'authored': '1915-04-21T00:00:00+00:00',
      'title': '\nThe\n\nSecretary of State\n\nto the British Ambassador (\nSpring Rice\n)'}]
    >>> hl.hlab_entity(collection = 'frus', country = 'Belize', summary = True, run = True)
    [{'entity_type': 'country',
      'entity_id': '084',
      'entity_name': 'Belize',
      'corpus': 'frus',
      'ref_cnt': 247}]
    """
    # Checks
    check_bool(run)
    check_bool(country_or)
    check_bool(topic_or)
    check_bool(person_or)
    check_bool(summary)
    assert isinstance(limit, int) == True, "Value of parameter 'limit' must be an integer"
    check_fields(fields)
    if date and (start_date or end_date):
        raise Exception("You cannot specify both a date and a start or end date")
    check_date(start_date)
    check_date(end_date)
    check_date(date)
    check_date_range(start_date, end_date)
    if not country and not topic and not person:
        raise Exception("No entities provided, please supply at least one entity in the country, topics and/or person fields")
    if summary == True and (date or start_date or end_date):
        raise Exception("Date filters not applicable when querying for a summary")
    # Creating URL
    url = "http://api.foiarchive.org/"
    if summary == False:
        url = url + 'documents?'
        if country:
            country = convert_to_list(country)
            url = url + 'countries=' + entity_url_creator(country, country_or) + '&'
        if topic:
            topic = convert_to_list(topic)
            url = url + 'topics=' + entity_url_creator(topic, topic_or) + '&'
        if person:
            person = convert_to_list(person)
            url = url + 'person_ids=' + entity_url_creator(person, person_or) + '&'
        url = url[:len(url)-1]
        if not fields:
            fields = ['doc_id', 'authored', 'title']
        else:
            fields = convert_to_list(fields)
        url = url + '&select='
        for i in fields:
            url = url + i + ","
        url = url[:len(url)-1] 
    else:
        if not country:
            count_country = 0
        else:
            country = convert_to_list(country)
            count_country = len(country)
        if not topic:
            count_topic = 0
        else:
            topic = convert_to_list(topic)
            count_topic = len(topic)
        if not person:
            count_person = 0
        else:
            person = convert_to_list(person)
            count_person = len(person)
        if count_country + count_topic + count_person > 1:
            raise Exception("Only a single entity value may be used with a summary search")
        if country:
            url = url + "entities?entity_type=eq.country&entity_name=ilike.*" + config_ent(country) + "*"
        if topic:
            url = url + "entities?entity_type=topic&entity_name=ilike.*" + config_ent(topic) + "*"
        if person:
            url = url + "entities?entity_type=eq.person&entity_name=ilike.*" + config_ent(person) + "*"
    if collection:
        check_collection(collection)
        url = url + '&corpus=eq.' + collection
    if summary == False:
        if date:
            url = url + '&authored=eq.' + date
        if start_date and end_date:
            url = url + '&authored=gte.' + start_date + '&authored=lte.' + end_date
    url = url + '&limit=' + str(limit)
    if run == False:
        return(url)
    else:
        return hlab_results(url)
    
    
def hlab_date(date = None, start_date = None, end_date = None, fields = None, collection = None, limit = 25, run = False):
    """
    A function that allows users to search for documents based on the dates when they were published.
    
    Parameters
    ----------
    date: String (in the YYYY-MM-DD format)
        A string specifying the exact date of the documents this function will search for. 
        Mutually exclusive with the start_date and end_date parameters.
    start_date: String (in the YYYY-MM-DD format)
        A string specifying the start of the date range of the documents which this function will search for. 
        Need to provide an end date as well if using this.
    end_date: String (in the YYYY-MM-DD format)
        A string specifying the end of the date range of the documents which this function will search for. 
        Need to provide a start date as well if using this.
    fields: String or list
        Series of fields that the user wants to display for each document that the search function finds. 
        Can be input as a list if the user wishes to have multiple fields displayed. If no field is provided,
        the function defaults to displaying the doc_id, authored, and title fields.
    collection: String    
        A string that can be used to filter results to a specific document collection (eg. 'frus').
    limit: Integer
        An integer specifying the maximum number of documents this function will display. The default limit is 25.
    run: Bool
        If False, function will only return the API URL. If True, function will return the JSON object that 
        is generated by the full API query.
        
    Returns
    -------
    Either a string specifying the URL that is needed to query the desired results from the API, or a JSON object 
    containing the list of all the documents - along with the specified fields - that match the search query that 
    the function generates.
    
    Examples
    --------
    >>> from histlabapi import histlabapi as hl
    >>> hl.hlab_date(date = '1955-01-20', collection = 'frus', limit = 5, run = False)
    'http://api.foiarchive.org/documents?&authored=eq.1955-01-20&select=doc_id,authored,title&corpus=eq.frus&limit=5'
    >>> hl.hlab_date(date = '1955-01-20', collection = 'frus', limit = 5, run = True)
    [{'doc_id': 'frus1955-57v01d24',
      'authored': '1955-01-20T00:00:00+00:00',
      'title': '24. Memorandum From the Special Representative in Vietnam (Collins) to the Secretary of State'},
     {'doc_id': 'frus1955-57v02d24',
      'authored': '1955-01-20T00:00:00+00:00',
      'title': '24. Draft Message From the President to the\n                                Congress'},
     {'doc_id': 'frus1955-57v01d23',
      'authored': '1955-01-20T00:00:00+00:00',
      'title': '23. Letter From the Counselor of the Department of State (MacArthur) to the Chargé in France (Achilles)'},
     {'doc_id': 'frus1955-57v07d420',
      'authored': '1955-01-20T00:00:00+00:00',
      'title': '420. Memorandum From Albert H.\n                                Gerberich of the Office of South American Affairs to the\n                            Director of the Office (Atwood)'},
     {'doc_id': 'frus1955-57v07d92',
      'authored': '1955-01-20T00:00:00+00:00',
      'title': '92. Memorandum of a Conversation, Department of State, Washington,\n                            January 20, 1955'}] 
    >>> hl.hlab_date(start_date = '1960-01-01', end_date = '1980-01-01', collection = 'frus', limit = 5, run = True)
    [{'doc_id': 'frus1865p4d173',
      'authored': None,
      'title': '[From the Avenir National, April 28, 1865.]'},
     {'doc_id': 'frus1865p4d188',
      'authored': None,
      'title': '[From La France, May 3, 1865.]'},
     {'doc_id': 'frus1865p4d18',
      'authored': None,
      'title': 'American Residents of Buenos Ayres'},
     {'doc_id': 'frus1865p4d193',
      'authored': None,
      'title': '[From the Journal des Debats, April 28, 1865.]'},
     {'doc_id': 'frus1865p4d194',
      'authored': None,
      'title': '[From the Journal des Debats, April 29, 1865.]'}]
    """
    # Checks
    check_bool(run)
    assert isinstance(limit, int) == True, "Value of parameter 'limit' must be an integer"
    check_fields(fields)
    if date and (start_date or end_date):
        raise Exception("You cannot specify both a date and a start or end date")
    check_date(start_date)
    check_date(end_date)
    check_date(date)
    check_date_range(start_date, end_date)
    # Create URL
    url = "http://api.foiarchive.org/documents?"
    if date:
            url = url + '&authored=eq.' + date
    if start_date and end_date:
        url = url + '&authored=gte.' + start_date + '&authored=lte.' + end_date
    if not fields:
        fields = ['doc_id', 'authored', 'title']
    else:
        fields = convert_to_list(fields)
    url = url + '&select='
    for i in fields:
        url = url + i + ","
    url = url[:len(url)-1]
    if collection:
        check_collection(collection)
        url = url + '&corpus=eq.' + collection
    url = url + '&limit=' + str(limit)
    if run == False:
        return(url)
    else:
        return hlab_results(url)
    
    
def hlab_id(ids, fields = None, run = False):
    """
    A function that allows users to search documents by their ID number
    
    Parameters
    ----------
    ids: String or list
        The specific IDs of the documents users want to search. Can be input as a list if the user wishes 
        to search for multipled IDs
    fields: String or list
        Series of fields that the user wants to display for each document that the search function finds. 
        Can be input as a list if the user wishes to have multiple fields displayed. If no field is provided, 
        the function defaults to displaying the doc_id, authored, and title fields.
    run: Bool
        If False, function will only return the API URL. If True, function will return the JSON object that 
        is generated by the full API query.
        
    Returns
    -------
    Either a string specifying the URL that is needed to query the desired results from the API, or a 
    JSON object containing the list of all the documents - along with the specified fields - that match 
    the search query that the function generates.
    
    Examples
    --------
    >>> from histlabapi import histlabapi as hl
    >>> hl.hlab_search_id(ids = 'frus1969-76ve05p1d11', fields = ['doc_id','body','title',"persons"], run = False)
    'http://api.foiarchive.org/documents?doc_id=in.(frus1969-76ve05p1d11)&select=doc_id,body,title,persons'
    >>> hl.hlab_search_id(ids = 'frus1969-76ve05p1d11', fields = ['doc_id','title',"persons"], run = True)
    [{'doc_id': 'frus1969-76ve05p1d11',
      'title': '11. Letter From Secretary of State Rogers to President Nixon, Washington, March 26,\n                                1970\n\n',
      'persons': ['Nixon, Richard M.', 'Rogers, William Pierce']}]
    >>> hl.hlab_search_id(ids = ['frus1969-76ve05p1d11','frus1958-60v03d44'], fields = ['doc_id','title',"topics","countries"], run = True)
    [{'doc_id': 'frus1958-60v03d44',
      'title': '44. Memorandum of Conference With President Eisenhower',
      'topics': None,
      'countries': None},
     {'doc_id': 'frus1969-76ve05p1d11',
      'title': '11. Letter From Secretary of State Rogers to President Nixon, Washington, March 26,\n                                1970\n\n',
      'topics': ['Argentine and Brazil Relations',
       'Relations with Tunisia',
       'Support for International Organizations'],
      'countries': ['Ethiopia',
       'Liberia',
       'Mauritania',
       'Morocco',
       'Namibia',
       'Portugal',
       'South Africa',
       'Tunisia',
       'United States']}]
    """
    # Checks
    check_bool(run)
    check_fields(fields)
    # Create URL
    url = "http://api.foiarchive.org/documents?doc_id=in.("
    ids = convert_to_list(ids)
    for i in ids:
        url = url + i + ","
    url = url[:len(url)-1] + ")"
    if not fields:
        fields = ['doc_id', 'authored', 'title']
    else:
        fields = convert_to_list(fields)
    url = url + '&select='
    for i in fields:
        url = url + i + ","
    url = url[:len(url)-1]
    if run == False:
        return(url)
    else:
        return hlab_results(url)