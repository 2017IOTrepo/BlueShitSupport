import os
import asyncio
from pprint import pprint
import requests
import yaml
from pyquery import PyQuery

from video import Mp4info

config = None
titles = []
urls = []
res_id = []
loop = asyncio.get_event_loop()


def get(url, params=None):
    resp = requests.get(url=url, params=params, headers={
        'Cookie': config['url_config']['Cookie'],
        'User-Agent': config['url_config']['User-Agent'],
    })
    return resp.content if resp.status_code == 200 else None


def post(url, data=None):
    resp = requests.post(
        url=url,
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': config['url_config']['Cookie'],
            'User-Agent': config['url_config']['User-Agent'],
        }
    )
    return resp.content if resp.status_code == 200 else None


def file_write(name: str, data: list):
    file = open(f'cache/{name}.txt', 'w', encoding='utf8')
    file.write('\n'.join(data))
    file.close()


def config_load():
    global config
    config = yaml.load(
        open(r'config.yaml', encoding='utf8'),
        Loader=yaml.FullLoader
    )


def get_course_src():
    resp_text = get(
        config['url_config']['base_url'] + config['app']['course_id']
    )
    parser = PyQuery(resp_text)

    def fun_iter(i, element):
        dataIsDrag = parser(element) \
            .find('.res-info') \
            .find('.create-box') \
            .children()[-4] \
            .attrib['data-is-drag']

        if dataIsDrag == 'N':
            titles.append(
                parser(element)
                    .find('.res-info')
                    .find('.overflow-ellipsis')
                    .find('.res-name')
                    .text()
                    .strip()
            )
            urls.append(
                parser(element)
                    .attr('data-href')
                    .strip()
            )
            res_id.append(
                parser(element)
                    .attr('data-value')
                    .strip()
            )

    parser('.hide-div') \
        .children() \
        .each(fun_iter)

    file_write('urls', urls)
    file_write('titles', titles)
    file_write('res_id', res_id)


async def video_score(i):
    file = Mp4info(urls[i])
    d = file.get_duration()
    pprint(d)
    data = {
        'clazz_course_id': config['app']['course_id'],
        'res_id': res_id[i],
        'watch_to': int(d) + 1,
        'duration': int(d) + 1,
        'current_watch_to': 0
    }
    resp = post(
        url=config['url_config']['video_url'],
        data=data
    )
    pprint(str(i) + str(resp))


async def other_score(i):
    resp = get(url=urls[i])
    pprint(str(i) + str("normal_complete"))


async def score_async(i):
    ext = os.path.splitext(titles[i])[1]
    if ext == '.mp4':
        await video_score(i)
    else:
        await other_score(i)


def score_main():
    rate = int(config['app']['exp_speed'] / 2)
    for i in range(rate):
        loop.run_until_complete(score_async(i))


if __name__ == '__main__':
    pprint('--------读取配置文件--------')
    config_load()
    pprint(config)
    pprint('--------读取成功--------')
    pprint('--------获取网课资源列表--------')
    get_course_src()
    pprint('--------获取成功--------')
    pprint('--------开始刷资源--------')
    score_main()
