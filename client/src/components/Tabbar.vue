<template>
    <div class="tabbar">
        <button @click="navigateTo('rank')" :class="{ active: current === 'rank' }">成绩榜单</button>
        <button @click="navigateTo('predict')" :class="{ active: current === 'predict' }">成绩预测</button>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const current = ref('home')

const navigateTo = (page) => {
    current.value = page
    router.push(`/${page}`)
}
</script>

<style scoped>
.tabbar {
    display: flex;
    justify-content: space-around;
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #f7f7f7;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

button {
    flex: 1;
    padding: 10px 0;
    font-size: 16px;
    background: none;
    border: none;
    cursor: pointer;
}

button.active {
    color: #42b983;
}

button:hover {
    background-color: #eaeaea;
}
</style>