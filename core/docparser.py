def to_video(data):
    doc = dict()
    doc['type'] = 'video'
    doc['title'] = data['title']
    doc['video_id'] = data['video_id']
    doc['view_cnt'] = str(data['views'])
    doc['rating'] = str(data['rating'])
    doc['rating'] = str(data['rating'])
    doc['video_length'] = data['length']
    return doc


def to_playlist(data):
    def _get_id(url):
        querystring = url.split('?')[1]
        params = {qs.split('=')[0]: qs.split('=')[1] for qs in querystring.split('&')}
        return params['list']

    doc = dict()
    doc['type'] = 'playlist'
    doc['playlist_id'] = _get_id(data['url'])
    doc['video_ids'] = ' '.join(data['video_ids'])
    doc['video_cnt'] = len(data['video_ids'])
    return doc
