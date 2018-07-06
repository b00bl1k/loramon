<template>
    <div>
        <nav class="panel">
            <p class="panel-heading">Devices</p>
            <div class="panel-block">
                <p class="control has-icons-left">
                    <input v-model="keywords" class="input is-small" type="text" placeholder="Search by DevEUI">
                    <span class="icon is-small is-left">
                        <i class="fas fa-search" aria-hidden="true"></i>
                    </span>
                </p>
            </div>
            <a class="panel-block" v-for="result in results" :key="result.id">
                <span class="panel-icon">
                  <i class="fas fa-wifi" aria-hidden="true"></i>
                </span>
                {{ result.deveui }}
            </a>
        </nav>
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
            keywords: null,
            results: []
        }
    },

    created () {
        this.fetch()
    },

    watch: {
        keywords (after, before) {
            this.fetch()
        }
    },

    methods: {
        fetch () {
            var params = { params: { deveui: this.keywords, page: this.page } }
            axios.get('/api/devices', params)
                .then(response => {
                    this.results = response.data.devices
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

</style>
