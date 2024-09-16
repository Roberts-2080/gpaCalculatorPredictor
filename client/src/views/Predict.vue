<template>
    <div class="predict">
        <div class="header">
            <el-select v-model="semesterId" placeholder="学期" style="width: 240px" @change="handleSemesterChange">
                <el-option v-for="item in semesterList" :key="item.id" :label="item.title" :value="item.id" />
            </el-select>
        </div>

        <div class="content" v-loading="loading" v-if="semesterId != null">
            <div class="add-btn">
                <el-button class="btn" @click="showAdd">添加新科目预测</el-button>
            </div>
            <el-card class="content-item" v-for="item in courseList" shadow="hover">
                <template #header>
                    <div class="card-header">
                        <div class="card-header-title">
                            <span>{{ item.title }}</span>
                            <el-button class="btn" @click="toPredict(item)">去预测</el-button>
                        </div>
                    </div>
                </template>
                <div class="content-item-content">
                    <div class="content-item-conten-left">
                        <p class="content-item-text">Assessment数量：{{ item.assessment_count }}</p>
                        <p class="content-item-text">及格线：{{ item.pass_line }}%</p>
                    </div>
                    <div class="content-item-conten-right">
                        <el-button size="small" text @click="showDel(item.id)">删除</el-button>
                        <el-button size="small" text @click="showEdit(item)">编辑</el-button>
                    </div>
                </div>
            </el-card>
        </div>

        <el-dialog v-model="dialogFormVisible" :title="title" width="90%">
            <el-form :model="form">
                <el-form-item label="科目" :label-width="labelWidth" style="margin-right: 19px;">
                    <el-input v-model="form.title" autocomplete="off" />
                </el-form-item>
                <el-form-item label="及格线" :label-width="labelWidth" style="margin-right: 19px;">
                    <el-input v-model="form.pass_line" autocomplete="off" type="number" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取消</el-button>
                    <el-button class="btn" type="primary" @click="showSubmit">
                        保存
                    </el-button>
                </div>
            </template>
        </el-dialog>

    </div>
</template>
<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from '@/axios/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const semesterList = ref([])
const courseList = ref([])
const semesterId = ref(null)
const loading = ref(false)
const labelWidth = ref(60)

const del = async (id) => {
    try {
        const response = await axios.post('/api/course/v1/del', { id: id })
        return response

    } catch (error) {
        console.error('Failed to fetch rank data:', error)
    }
}

const toPredict = (item) => {
    router.push(`/to_predict?courseId=${item.id}&passLine=${item.pass_line}`)
}

const title = ref('')
const showAdd = () => {
    title.value = "添加科目"
    form.id = null
    form.title = ""
    form.pass_line = ""
    form.semester_id = semesterId.value
    dialogFormVisible.value = true
}

const form = reactive({
    id: null,
    title: "",
    pass_line: ""
})

const dialogFormVisible = ref(false)

const showDel = (id) => {
    ElMessageBox.confirm(
        '确定删除?',
        '提示',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    )
        .then(() => {
            del(id).then(res => {
                ElMessage({
                    type: 'success',
                    message: '删除成功',
                })
                handleSemesterChange()
            })
        })
}

const showEdit = (item) => {
    title.value = "编辑科目"
    form.id = item.id
    form.title = item.title
    form.pass_line = item.pass_line
    dialogFormVisible.value = true
}

const fetchSemesterData = async () => {
    try {
        const response = await axios.post('/api/semester/v1/list')
        semesterList.value = response.data.data
        semesterId.value = semesterList.value[0]?.id
        handleSemesterChange()
    } catch (error) {
        console.error(error)
    }
}

const handleSemesterChange = async () => {
    try {
        loading.value = true
        const response = await axios.post('/api/course/v1/list', { id: semesterId.value })
        courseList.value = response.data.data
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

const editCourse = async () => {
    try {
        const response = await axios.post('/api/course/v1/update', form)
        return response

    } catch (error) {

    }
}

const addCourse = async () => {
    try {
        const response = await axios.post('/api/course/v1/add', form)
        return response

    } catch (error) {

    }
}

const showSubmit = () => {
    ElMessageBox.confirm(
        '确定保存?',
        '提示',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    )
        .then(() => {
            if (title.value === "编辑科目") {
                editCourse().then(res => {
                    if (res.data.code === 0) {
                        ElMessage({
                            type: 'success',
                            message: '修改成功',
                        })
                        dialogFormVisible.value = false
                        handleSemesterChange()
                    } else {
                        ElMessage({
                            type: 'error',
                            message: res.data.msg,
                        })
                    }
                }).catch(error => {
                    ElMessage({
                        type: 'error',
                        message: error,
                    })
                })
            } else {
                addCourse().then(res => {
                    if (res.data.code === 0) {
                        ElMessage({
                            type: 'success',
                            message: '添加成功',
                        })
                        dialogFormVisible.value = false
                        handleSemesterChange()
                    } else {
                        ElMessage({
                            type: 'error',
                            message: res.data.msg,
                        })
                    }
                }).catch(error => {
                    ElMessage({
                        type: 'error',
                        message: error,
                    })
                })
            }

        })
}

onMounted(async () => {
    await fetchSemesterData()
})
</script>
<style scoped>
.predict {
    flex: 1;
    padding-bottom: 40px;
}

.header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgb(118, 124, 180);
    height: 80px;
    width: 100%;
}

.content {
    margin: 10px 10px 0 10px;
}

.content-item {
    margin-top: 10px;
}

.content-item-text {
    font-size: 12px;
}

.card-header-title {
    display: flex;
    justify-content: space-between;
    align-items: center
}

.content-item-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.add-btn {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.btn {
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}

.btn:active,
.btn:focus,
.btn:hover {
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}
</style>