import * as mysql from 'mysql'

/**
 * 封装一个数据库连接的方法
 * @param {string} sql SQL语句
 * @param arg SQL语句插入语句的数据
 * @param callback SQL语句的回调
 */
export function db(sql: string, arg: any, callback?: any) {
    // 1.创建连接
    const config = mysql.createConnection({
        host: '', // 数据库地址
        user: '', // 数据库名
        password: '', // 数据库密码
        port: 3306, // 端口号
        database: '' // 使用数据库名字
    });
    // 2.开始连接数据库
    config.connect();
    // 3.封装对数据库的增删改查操作
    config.query(sql, arg, (err: any, data: any) => {
        callback(err, data);
    });
    // 4.关闭数据库
    config.end();
}

/* 异步延时函数 需要await */
export function sleep(msec: number) {
    return new Promise<void>(resolve => setTimeout(resolve, msec));
}
