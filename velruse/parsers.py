"""Parsers to extract data and normalize it per Portable Contacts format"""
def extract_fb_data(data):
    """Extact and normalize facebook data as parsed from the graph JSON"""
    # Setup the normalized contact info
    nick = None
    
    # Setup the nick and preferred username to the last portion of the
    # FB link URL if its not their ID
    link = data.get('link')
    if link:
        last = link.split('/')[-1]
        if last != data['id']:
            nick = last
    
    profile = {
        'providerName': 'Facebook',
        'identifier': 'https://graph.facebook.com/%s' % data['id'],
        'displayName': data['name'],
        'emails': [data.get('email')],
        'verifiedEmail': data.get('email') if data.get('verified') else False,
        'gender': data.get('gender'),
        'preferredUsername': nick or data['name'],
    }
    tz = data.get('timezone')
    if tz:
        parts = str(tz).split(':')
        if len(parts) > 1:
            h, m = parts
        else:
            h, m = parts[0], '00'
        if 1 < len(h) < 3:
            h = '%s0%s' % (h[0], h[1])
        elif len(h) == 1:
            h = h[0]
        data['utfOffset'] = ':'.join([h, m])
    bday = data.get('birthday')
    if bday:
        mth, day, yr = bday.split('/')
        profile['birthday'] = '-'.join([yr, mth, day])
    name = {}
    pcard_map = {'first_name': 'givenName', 'last_name': 'familyName'}
    for key, val in pcard_map.items():
        part = data.get(key)
        if part:
            name[val] = part
    name['formatted'] = data.get('name')
    
    profile['name'] = name
    
    # Now strip out empty values
    for k, v in profile.items():
        if not v or (isinstance(v, list) and not v[0]):
            del profile[k]
    
    return profile
