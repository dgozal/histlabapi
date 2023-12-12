from histlabapi import histlabapi as hl

def test_list_collections():
    test = [{'corpus': 'frus', 'doc_cnt': 209046},
     {'corpus': 'cia', 'doc_cnt': 935716},
     {'corpus': 'clinton', 'doc_cnt': 54149},
     {'corpus': 'pdb', 'doc_cnt': 5011},
     {'corpus': 'cfpf', 'doc_cnt': 3214293},
     {'corpus': 'kissinger', 'doc_cnt': 4552},
     {'corpus': 'nato', 'doc_cnt': 46002}]
    assert hl.list_collections() == test
    
def test_hlab_overview():
    test_url = 'http://api.foiarchive.org/entities?entity_type=eq.person&corpus=eq.frus&limit=5'
    test = [{'entity_type': 'person',
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
    assert test_url == hl.hlab_overview(collection = 'frus', sort = None, entity_type = 'person', limit = 5, run = False)
    assert test == hl.hlab_overview(collection = 'frus', sort = None, entity_type = 'person', limit = 5, run = True)
    
def test_hlab_search():
    test_url = 'http://api.foiarchive.org/documents?and=(full_text.phfts.league%20of%20nations)&select=doc_id,authored,title&limit=25'
    test = [{'doc_id': '0000BA89',
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
    assert test_url == hl.hlab_search('league of nations', run = False)
    assert test == hl.hlab_search(['league of nations', 'trade'], fields = ['doc_id', 'title', 'countries'], join_or = True, limit = 5, run = True)
    
def test_find_entity_id():
    test1 = [{'country_name': 'Indonesia', 'country_id': '360'}]
    test2 = [{'full_name': 'Nixon, Patricia', 'person_id': '109881'},
     {'full_name': 'Nixon, Richard M.', 'person_id': '109882'},
     {'full_name': 'Nixon, Robert', 'person_id': '109883'},
     {'full_name': 'Nixon, Patricia', 'person_id': 'hrc5592'},
     {'full_name': 'Nixon, Richard; Nixon, Richard M.; Nixon, Richard Milhouse',
      'person_id': 'hrc5593'},
     {'full_name': 'Cox, Tricia Nixon', 'person_id': 'hrc10032'},
     {'full_name': 'Cox, Tricia Nixon', 'person_id': 'kiss10032'},
     {'full_name': 'Nixon, Richard; Nixon, Richard M.; Nixon, Richard Milhouse',
      'person_id': 'kiss109882'}]
    assert test1 == hl.find_entity_id('country', 'Indonesia')
    assert test2 == hl.find_entity_id('person', 'Nixon')
    
def test_hlab_entity():
    test_url = 'http://api.foiarchive.org/documents?countries=cs.{Belize}&select=doc_id,authored,title&corpus=eq.frus&limit=5'
    test1 = [{'doc_id': 'frus1865p4d471',
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
    test2 = [{'entity_type': 'country',
      'entity_id': '084',
      'entity_name': 'Belize',
      'corpus': 'frus',
      'ref_cnt': 247}]
    assert test_url == hl.hlab_entity(collection = 'frus', country = 'Belize', run = False, limit = 5)
    assert test1 == hl.hlab_entity(collection = 'frus', country = 'Belize', run = True, limit = 5)
    assert test2 == hl.hlab_entity(collection = 'frus', country = 'Belize', summary = True, run = True)
    
def test_hlab_date():
    test_url = 'http://api.foiarchive.org/documents?&authored=eq.1955-01-20&select=doc_id,authored,title&corpus=eq.frus&limit=5'
    test1 = [{'doc_id': 'frus1955-57v01d24',
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
    test2 = [{'doc_id': 'frus1865p4d173',
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
    assert test_url == hl.hlab_date(date = '1955-01-20', collection = 'frus', limit = 5, run = False)
    assert test1 == hl.hlab_date(date = '1955-01-20', collection = 'frus', limit = 5, run = True)
    assert test2 == hl.hlab_date(start_date = '1960-01-01', end_date = '1980-01-01', collection = 'frus', limit = 5, run = True)
    
def test_hlab_id():
    test_url = 'http://api.foiarchive.org/documents?doc_id=in.(frus1969-76ve05p1d11)&select=doc_id,body,title,persons'
    test1 = [{'doc_id': 'frus1969-76ve05p1d11',
      'title': '11. Letter From Secretary of State Rogers to President Nixon, Washington, March 26,\n                                1970\n\n',
      'persons': ['Nixon, Richard M.', 'Rogers, William Pierce']}]
    test2 = [{'doc_id': 'frus1958-60v03d44',
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
    assert test_url == hl.hlab_id(ids = 'frus1969-76ve05p1d11', fields = ['doc_id','body','title',"persons"], run = False)
    assert test1 == hl.hlab_id(ids = 'frus1969-76ve05p1d11', fields = ['doc_id','title',"persons"], run = True)
    assert test2 == hl.hlab_id(ids = ['frus1969-76ve05p1d11','frus1958-60v03d44'], fields = ['doc_id','title',"topics","countries"], run = True)