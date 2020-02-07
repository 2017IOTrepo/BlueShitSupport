import {remote_get} from "./api";
import * as cheerio from "cheerio";

const go = async () => {
    const res: any = await remote_get('https://www.douban.com/group/szsh/discussion?start=0');
    // 加载网页
    const $ = cheerio.load(res);
    let urls: string[] = [];
    let titles: string[] = [];
    // 获取网页中的数据，分别写到两个数组里面
    $('.olt').find('tr').find('.title')
        .find('a')
        .each((index, element) => {
            // @ts-ignore
            titles.push($(element).attr('title').trim());
            // @ts-ignore
            urls.push($(element).attr('href').trim());
        })
    // 打印数组
    console.log(titles, urls);
}

go();
