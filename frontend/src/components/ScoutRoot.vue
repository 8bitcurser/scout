<template>
    <div class="scoutRoot">
        <button v-on:click="load">Request Root</button>
        <span id="msg">{{ msg }}</span>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'ScoutRoot',
    data: function() {
        return {msg: 'Default!'}
    },
    methods: {
        load () {
            axios.get('http://localhost:8000/').then(
                (response) => {
                    this.msg = response.data;
                }
            )
        }   
    }    
}
</script>

<style scoped>
.scoutRoot {
    background-color: black;
    color: white;
}
#msg {
    display: block;
}
</style>