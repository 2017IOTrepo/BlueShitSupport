import {remote_get} from './api'
import * as cheerio from 'cheerio'
import {sleep} from "./util";
import jsyaml from "js-yaml"
import {readFileSync} from "fs";

export let config: any
const init = async () => {
    try {
        config = jsyaml.safeLoad(
            readFileSync('config.yaml', 'utf8')
        )
        console.log(config)
    } catch (e) {
        console.log(e)
    }
}

const fetchData = async () =>{
    await remote_get(config['url'])
}

init()
