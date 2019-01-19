import axios from 'axios'

var app = new Vue({
    el: '#app',
    data: {
          message: "hello"
    },

    mounted () {
        axios
          .get('https://api.coindesk.com/v1/bpi/currentprice.json')
          .then(response => (this.info = response))
      }
})