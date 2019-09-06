from pytube import YouTube, Playlist
from time import sleep


def _get_meta(youtube):
    meta = dict()
    meta['video_id'] = youtube.video_id
    meta['title'] = youtube.title
    meta['description'] = youtube.description
    meta['views'] = youtube.views
    meta['rating'] = youtube.rating
    meta['length'] = youtube.length
    # pytube bug - 직접 URL 입력
    meta['thumbnail_url'] = "https://img.youtube.com/vi/{}/maxresdefault.jpg".format(youtube.video_id)
    meta['embed_url'] = youtube.embed_url
    meta['age_restricted'] = youtube.age_restricted
    meta['watch_url'] = youtube.watch_url
    return meta


def _get_captions(youtube):
    captions = list()
    for cc in youtube.captions.all():
        captions.append([str(cc), str(cc.generate_srt_captions())])
    return captions


def from_youtube_url(url):
    yt = YouTube(url)
    meta = _get_meta(yt)
    captions = _get_captions(yt)

    output = dict()
    output['type'] = 'youtube'
    output['url'] = yt.watch_url
    output.update(meta)
    output['captions'] = captions

    return output


def from_playlist_url(url):
    pli = Playlist(url)
    pli.parse_links()
    pli.populate_video_urls()

    output = dict()
    output['type'] = 'playlist'
    output['title'] = pli.title()
    url = pli.construct_playlist_url()
    output['url'] = url
    output['playlist_id'] = _get_playlist_id(url)
    video_urls = pli.parse_links()
    output['video_urls'] = video_urls
    output['video_ids'] = [v.split('=')[1] for v in video_urls]
    return output


def _get_playlist_id(url):
    querystring = url.split('?')[1]
    params = {qs.split('=')[0]: qs.split('=')[1] for qs in querystring.split('&')}
    return params['list']


if __name__ == '__main__':
    print(_get_playlist_id('a'))
