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
            <router-link class="panel-block"
                :to="{ name: 'Device', params: { devId: result.id }}"
                v-for="result in results" :key="result.id">

                <span class="panel-icon">
                  <i class="fas fa-wifi" aria-hidden="true"></i>
                </span>
                {{ result.deveui }}
            </router-link>
        </nav>
        <nav v-if="pages > 1" class="pagination" role="navigation" aria-label="pagination">
            <ul class="pagination-list">
                <li v-for="n in pages" v-bind:key="n">
                    <router-link :to="{ name: 'IndexPaging', params: { page: n }}"
                        v-bind:class="{'pagination-link': true, 'is-current': page == n}"
                        aria-current="page">{{ n }}</router-link>
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
        '$route' (to, from) {
            this.fetch()
        },
        keywords (after, before) {
            this.fetch()
        }
    },

    methods: {
        fetch () {
            var params = {
                params: {
                    deveui: this.keywords,
                    page: this.$route.params.page
                }
            }
            axios.get('/api/devices', params)
                .then(response => {
                    this.results = response.data.devices
                    this.page = response.data.page
                    this.pages = response.data.pages
                })
                .catch(e => {

                })
        }
    }
}
</script>
