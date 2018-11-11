<template>
    <div>
        <table class="table is-fullwidth" id="log">
            <thead>
                <th style="width: 30%">Timestamp</th>
                <th style="width: 10%">SF</th>
                <th style="width: 10%">RSSI</th>
                <th style="width: 60%">Data</th>
            </thead>
            <tbody>
                <tr v-bind:class="'message-' + result.type" v-for="result in results" :key="result.id">
                    <td>{{ result.created }}</td>
                    <td>{{ result.txInfo.dataRate.spreadFactor }}</td>
                    <td>{{ result.rxInfo[0].rssi }}</td>
                    <td class="hex">
                        {{ result.data }}
                    </td>
                </tr>
            </tbody>
        </table>
        <infinite-loading @infinite="infiniteHandler">
            <span slot="no-more"></span>
        </infinite-loading>
    </div>
</template>

<script>
import InfiniteLoading from 'vue-infinite-loading'
import axios from 'axios'

export default {
    data () {
        return {
            page: 0,
            pages: 0,
            results: []
        }
    },

    methods: {
        infiniteHandler ($state) {
            if (this.page < this.pages || this.pages === 0) {
                this.page++
                var params = { params: { page: this.page } }
                axios.get('/api/device/' + this.$route.params.devId, params)
                    .then(response => {
                        this.results = this.results.concat(response.data.messages)
                        this.page = response.data.page
                        this.pages = response.data.pages
                        $state.loaded()
                    })
                    .catch(e => {

                    })
            } else {
                $state.complete()
            }
        }
    },

    components: {
        InfiniteLoading
    }
}
</script>

<style scoped>
.hex {
  font-family: monospace;
  font-size: 11pt;
}

.message-join {
  background-color: #dff0d8;
}

.message-uplink {

}
</style>
