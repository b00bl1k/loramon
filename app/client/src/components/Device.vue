<template>
    <div>
        <table class="table is-fullwidth" id="log">
            <thead>
                <th style="width: 30%">Timestamp</th>
                <th style="width: 10%">Type</th>
                <th style="width: 60%">Data</th>
            </thead>
            <tbody>
                <tr v-for="result in results" :key="result.id">
                    <td>{{ result.created }}</td>
                    <td>{{ result.type }}</td>
                    <td class="hex">
                        {{ result.data }}
                    </td>
                </tr>
            </tbody>
        </table>
        <nav v-if="pages > 1" class="pagination" role="navigation" aria-label="pagination">
            <ul class="pagination-list">
                <li v-for="n in pages" v-bind:key="n">
                    <a v-on:click="selectPage(n)"
                        v-bind:class="{'pagination-link': true, 'is-current': page == n}"
                        aria-current="page">{{ n }}</a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            page: 0,
            pages: 0,
            results: []
        }
    },

    created () {
        this.fetch()
    },

    methods: {
        fetch () {
            var params = { params: { deveui: this.keywords, page: this.page } }
            axios.get('/api/device/' + this.$route.params.devId, params)
                .then(response => {
                    this.results = response.data.messages
                    this.page = response.data.page
                    this.pages = response.data.pages
                })
                .catch(e => {

                })
        },

        selectPage (nPage) {
            this.page = nPage
            this.fetch()
        }
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
