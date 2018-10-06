'use strict';

const url = require('url');
const {
    stringify
} = require('querystring');
const axios = require('axios');
const camelcaseKeys = require('camelcase-keys');
const decamelizeKeys = require('decamelize-keys');
const router = require('./route.js');

axios.defaults.baseURL = 'http://localhost:5000/api';
axios.defaults.auth = {
    username: '',
    password: ''
};

axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response) {
        switch (error.response.status) {
            case 401:
                store.commit('del_token')
                router.push('/login')
        }
    }
    return Promise.reject(error.response.data)
})

router.beforeEach((to, from, next) => {
    if (to.meta.required) {
        // 检查localStorage
        if (localStorage.token) {
            store.commit('set_token', localStorage.token)
            // 添加axios头部Authorized
            axios.defaults.auth = {
                username: store.state.token,
                password: store.state.token,
            }
            // iview的页面加载条
            iView.LoadingBar.start();
            next()
        } else {
            next({
                path: '/login',
            })
        }
    } else {
        iView.LoadingBar.start();
        next()
    }
})

class YabeApp {
    constructor(username, password) {
        this.username = username;
        this.password = password;
        this.token = '';
        // -- wait -- //
    }

    login(username, password) {
        this.username = username || this.username;
        this.password = password || this.password;

        if (typeof this.username !== 'string') {
            return Promise.reject(
                new TypeError(`Excepted a string, got ${typeof this.username}`)
            );
        }
        if (typeof this.password !== 'string') {
            return Promise.reject(
                new TypeError(`Excepted a string, got ${typeof this.password}`);
            );
        }
    }
}