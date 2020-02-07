import {remote_get, remote_post} from './api'
import * as cheerio from 'cheerio'
import {sleep} from "./util";
import jsyaml from "js-yaml"
import {existsSync, readFileSync, writeFileSync} from "fs";
import {stringify} from "querystring";

export let config: any
let urls: string[] = [];
let titles: string[] = [];

const init = async () => {
    try {
        config = jsyaml.safeLoad(
            readFileSync('config.yaml', 'utf8')
        ).app
        console.log(config)
    } catch (e) {
        console.log(e)
    }
}

const fetchData = async () => {
    const res: any = await remote_get(config['url'] + config['crouse_id'])
    // console.log(res)
    const $ = cheerio.load(res);
    // 获取网页中的数据，分别写到两个数组里面
    $('.hide-div')
        .children()
        .each((index, element) => {
            let dataIsDrag = $(element)
                .find('.res-info')
                .find('.create-box')
                .children()
                .get().slice(-3, -2)[0]
                .attribs['data-is-drag']

            if (dataIsDrag == 'N') {
                titles.push(
                    // @ts-ignore
                    $(element)
                        .find('.res-info')
                        .find('.overflow-ellipsis')
                        .find('span')
                        .attr('title')
                        .trim()
                );
                // @ts-ignore
                urls.push($(element).attr('data-href').trim());
            }
        })
    // 打印数组
    console.log(titles, urls);
    writeFileSync('cache/title.txt', titles)
    writeFileSync('cache/urls.txt', urls)
    writeFileSync('cache/src_page.html', res)
}

const scoreScriptStart = async () => {

}

const main = async () => {
    await init()
    if (
        existsSync('cache/title.txt') &&
        existsSync('cache/urls.txt')
    ) {
        console.log('--------正在从已知文件中读取---------')
        urls = readFileSync('cache/urls.txt')
            .toString().split(',')
        titles = readFileSync('cache/title.txt')
            .toString().split(',')
        console.log(titles, urls)
    } else {
        console.log('--------正在网站中读取---------')
        await fetchData()
    }

    scoreScriptStart()
}

main()
// init()
// fetchData()
