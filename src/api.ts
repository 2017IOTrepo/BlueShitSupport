import axios from 'axios'

/**网络请求 */
export const remote_get = function (url: string) {
    const promise = new Promise(function (resolve, reject) {
        axios.get(url).then((res: any) => {
            resolve(res.data);
        }, (err: any) => {
            reject(err);
        });
    });
    return promise;
}
