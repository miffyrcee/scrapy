import json
import os
import re
import urllib
from multiprocessing import Pool, Queue
from random import choice

import requests

os.environ['ALL_PROXY'] = 'http://127.0.0.1:8090'

token = ''
viewkey = ''
sess = requests.Session()

cwd = os.path.dirname(__file__)
fp = os.path.join(cwd, 'agent.json')
with open(fp, 'r') as fr:
    agent = json.loads(fr.read())


def get_agent(agent):
    _agent = choice(agent['Headers']['User-Agent'])
    return _agent


def save_ts(viedo_url):
    r = sess.get(viedo_url, headers={'User-Agent': get_agent(agent)})
    suffix = os.path.basename(viedo_url)
    suffix = 'girls'
    if not os.path.exists(suffix):
        os.mkdir(suffix)
    fn = viedo_url.split('/')[-1]
    print(fn)
    with open(os.path.join(suffix, fn), 'wb') as fw:
        fw.write(r.content)


def get_m3u8(home_url):
    r = sess.get(home_url, headers={'User-Agent': get_agent(agent)})
    text = re.findall("http.*m3u8.*\'", r.text)
    m3u8_url = text[0].strip('\'')
    return m3u8_url


def get_max_resolution(m3u8_url):
    r = sess.get(m3u8_url, headers={'User-Agent': get_agent(agent)})
    text = re.findall('hls.*', r.text)
    fn = max(text, key=lambda url: url.split('-')[1][:-1])
    max_frame_url = os.path.join(os.path.dirname(m3u8_url), fn)
    return max_frame_url


def get_tss(max_resolution_url):
    r = sess.get(max_resolution_url, headers={'User-Agent': get_agent(agent)})
    ts_fns = re.findall('hls.*ts', r.text)

    def get_whole_url(ts_fn):
        whole_url = os.path.join(os.path.dirname(max_resolution_url), ts_fn)
        return whole_url

    ts_urls = list(map(get_whole_url, ts_fns))
    return ts_urls


m3u8_url = get_m3u8(
    'https://www.xvideos.com/video34804229/bigo_._nua_em_them_xoac')
max_resolution = get_max_resolution(m3u8_url)
ts_urls = get_tss(max_resolution)
if __name__ == "__main__":
    urls = ts_urls

    # with Pool(processes=4) as pool:
    #     res = [pool.apply_async(save_ts, (_url, )) for _url in urls]
    #     [r.get() for r in res]
    for i in urls:
        save_ts(i)
