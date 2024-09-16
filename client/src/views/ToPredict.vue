<template>
    <div class="to-predict">
        <div class="header">
            <div class="back-btn" @click="toBack">
                <el-icon>
                    <ArrowLeft />
                </el-icon>
                <span style="margin-left: 5px;">返回</span>
            </div>
        </div>

        <div class="container" v-loading="loading">
            <el-card class="container-item" v-for="item in moduleList" shadow="hover">
                <template #header>
                    <div class="card-header">
                        <div class="card-header-title">
                            <span>{{ item.title }}</span>
                            <!-- <el-button class="btn" @click="toPredict(item.id)">去预测</el-button> -->
                        </div>
                        <span v-if="!item.grade_percentage || !item.test_score || !item.current_score"
                            class="card-header-info">*信息不完整</span>
                    </div>
                </template>
                <div class="container-item-content">
                    <span class="container-item-content-text">成绩占比：<span v-if="item.grade_percentage">{{
                item.grade_percentage
            }}%</span><span v-else>未知</span></span>
                    <span class="container-item-content-text">测试满分：<span v-if="item.test_score">{{
                item.test_score
            }}分</span><span v-else>未知</span></span>
                    <span class="container-item-content-text">已得分数：<span v-if="item.current_score">{{
                item.current_score
            }}%</span><span v-else>未知</span></span>
                </div>
                <div class="card-btn">
                    <el-button @click="showDel(item.id)">删除</el-button>
                    <el-button type="primary" @click="showEdit(item)">编辑</el-button>
                </div>
            </el-card>
        </div>
        <div>
            <div class="bottom-content">
                <el-card shadow="hover" class="bottom-card">
                    <template #header>
                        <div class="bottom-content-title">
                            <div class="bottom-content-title-text">
                                <div style="color: aliceblue; font-size: 14px;">
                                    最终测试 - {{ testForm.title }}
                                </div>
                                <div style="color: beige; font-size: 12px; margin-top: 5px;">
                                    <span>成绩占比: {{ testForm.test_percentage }}%</span>&nbsp;&nbsp;&nbsp;
                                    <span>测试满分: {{ testForm.test_score }}分</span>
                                </div>
                            </div>
                            <div>
                                <el-button @click="showEditTest">编辑</el-button>
                            </div>
                        </div>
                    </template>
                    <div>
                        <div style="color: beige; font-size: 12px; margin-top: 5px;">
                            <span>你对通过本课程最终的预期(预测前请选择)</span>&nbsp;&nbsp;&nbsp;
                        </div>
                        <div
                            style="display: flex; justify-content: flex-start; flex-direction: row; align-items: center; color: beige;">
                            <el-radio-group v-model="radio1">
                                <el-radio :value="1" size="large">不挂科（{{ passLine }}%）</el-radio>
                                <el-radio :value="2" size="large">得高分</el-radio>
                            </el-radio-group>
                            <el-input style="width: 30%; height: 20px; margin-left: 5px;" size="small"
                                :disabled="radio1 === 1" v-model="testForm.prediction_line" type="number"></el-input>
                        </div>
                    </div>
                </el-card>
            </div>
            <div class="bottom-btn">
                <el-button type="primary" @click="showAdd">添加新任务</el-button>
                <el-button class="btn" @click="predict">立即预测</el-button>
            </div>
        </div>

        <el-dialog v-model="dialogFormVisible" :title="title" width="90%">
            <el-form :model="form">
                <el-form-item label="任务" :label-width="labelWidth">
                    <el-input v-model="form.title" autocomplete="off" />
                </el-form-item>
                <el-form-item label="成绩占比" :label-width="labelWidth">
                    <el-input v-model="form.grade_percentage" autocomplete="off" type="number" />
                </el-form-item>
                <el-form-item label="测试满分" :label-width="labelWidth">
                    <el-input v-model="form.test_score" autocomplete="off" type="number" />
                </el-form-item>
                <el-form-item label="已得分数" :label-width="labelWidth">
                    <el-input v-model="form.current_score" autocomplete="off" type="number" />
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

        <el-dialog v-model="testDialogFormVisible" title="修改测试任务" width="90%">
            <el-form :model="testForm">
                <el-form-item label="任务" :label-width="labelWidth">
                    <el-input v-model="testForm.title" autocomplete="off" />
                </el-form-item>
                <el-form-item label="成绩占比" :label-width="labelWidth">
                    <el-input v-model="testForm.test_percentage" autocomplete="off" type="number" />
                </el-form-item>
                <el-form-item label="测试满分" :label-width="labelWidth">
                    <el-input v-model="testForm.test_score" autocomplete="off" type="number" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="testDialogFormVisible = false">取消</el-button>
                    <el-button class="btn" type="primary" @click="testDialogFormVisible = false">
                        保存
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <el-dialog v-model="resultDialogFormVisible" width="90%">
            <div class="result-bg" ref="screenshotArea">
                <div style="margin: 10px">
                    <h3>您需要获得{{result}}的分数</h3>
                </div>
                <el-icon class="share-btn" @click="captureScreenShot">
                    <Share />
                </el-icon>
            </div>
        </el-dialog>
    </div>
</template>
<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from '@/axios/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import html2canvas from "html2canvas";

const route = useRoute()
const router = useRouter()
const courseId = route.query.courseId
const passLine = route.query.passLine
const loading = ref(false)
const labelWidth = ref(80)
const moduleList = ref([])
const dialogFormVisible = ref(false)
const title = ref('')
const form = reactive({
    course_id: null,
    title: '',
    current_score: '',
    grade_percentage: '',
    test_score: '',
})

const resultDialogFormVisible = ref(false)
const screenshotArea = ref('')
const captureScreenShot = () => {
    if (screenshotArea.value) {
        html2canvas(screenshotArea.value).then((canvas) => {
            // 将 canvas 转换为 base64 并存储在 screenshot 中
            const screenshot = canvas.toDataURL('image/png');
            // 创建一个临时的 <a> 元素用于下载
            const link = document.createElement('a');
            link.href = screenshot;
            link.download = 'result.png';  // 下载文件的默认名称
            // 模拟点击下载
            link.click();
        });
    }
};
const showTestSubmit = async () => { }

const showEditTest = () => {
    testDialogFormVisible.value = true
}
const testDialogFormVisible = ref(false)

const radio1 = ref(1)

const testForm = reactive({
    course_id: null,
    title: "Exam",
    prediction_line: "",  // 
    test_percentage: "",  // 
    test_score: ""  // 测试满分, 没用
})

const result = ref('')

const predict = async () => {
    for (let i = 0; i < moduleList.value.length; i++) {
        if (!moduleList.value[i].current_score || !moduleList.value[i].test_score) {
            return ElMessage({
                type: 'error',
                message: '信息不完整, 请补充信息',
            })
        }
    }
    console.log(radio1.value);

    if (radio1.value === 1) {
        console.log(testForm);
        testForm.prediction_line = passLine
        if (!testForm.test_percentage) {
            return ElMessage({
                type: 'error',
                message: '测试成绩占比不能为空',
            })
        }
    } else {
        if (!testForm.prediction_line || !testForm.test_percentage) {
            return ElMessage({
                type: 'error',
                message: '测试成绩占比或预期线不能为空',
            })
        }
    }
    testForm.course_id = courseId
    try {
        const response = await axios.post('/api/score/v1/predict', testForm)
        console.log(response);
        if (response.data.code !== 0) {
            return ElMessage.error(response.data.msg)
        } else {
            result.value = response.data.data

            resultDialogFormVisible.value = true
        }
    } catch (error) {
        console.error(error)
    } finally {
    }
}

const toBack = () => {
    router.back()
}

const showAdd = () => {
    form.course_id = courseId
    form.title = ''
    form.current_score = ''
    form.grade_percentage = ''
    form.test_score = ''
    title.value = "添加任务"
    dialogFormVisible.value = true
}

const addModule = async () => {
    try {
        const response = await axios.post('/api/module/v1/add', form)
        return response
    } catch (error) {
        console.error(error)
    } finally {
    }
}

const editModule = async () => {
    try {
        const response = await axios.post('/api/module/v1/update', form)
        return response
    } catch (error) {
        console.error(error)
    } finally {

    }
}

const showEdit = (row) => {
    title.value = "修改任务"
    form.title = row.title
    form.current_score = row.current_score
    form.grade_percentage = row.grade_percentage
    form.test_score = row.test_score
    form.course_id = courseId
    form["id"] = row.id
    dialogFormVisible.value = true
}

const showSubmit = async () => {
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
            if (title.value === "修改任务") {
                editModule().then(res => {
                    if (res.data.code === 0) {
                        ElMessage({
                            type: 'success',
                            message: '修改成功',
                        })
                        dialogFormVisible.value = false
                        fetchModuleData()
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
                addModule().then(res => {
                    if (res.data.code === 0) {
                        ElMessage({
                            type: 'success',
                            message: '添加成功',
                        })
                        dialogFormVisible.value = false
                        fetchModuleData()
                    } else {
                        ElMessage({
                            type: 'error',
                            message: res.data.msg,
                        })
                    }
                })
            }

        })
}


const fetchModuleData = async () => {
    try {
        loading.value = true
        const response = await axios.post('/api/module/v1/list', { course_id: courseId })
        moduleList.value = response.data.data
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

const del = async (id) => {
    try {
        const response = await axios.post('/api/module/v1/del', { id: id })
        return response

    } catch (error) {
        console.error(error)
    }
}


const showDel = async (id) => {
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
                fetchModuleData()
            })
        })
}


fetchModuleData()

onMounted(() => {

})
</script>
<style scoped>
.to-predict {
    flex: 1;
    padding-bottom: 40px;
}


:deep(.el-radio__label) {
    color: beige;
}

.bottom-content-title {
    display: flex;
    justify-content: space-between;
}

.header {
    margin: 10px;
}

.container {
    display: flex;
    flex-wrap: wrap;
    margin: 5px
}

.container-item {
    flex: 0 0 calc(47%);
    /* 每个元素占50%的宽度，减去间距 */
    box-sizing: border-box;
    margin: 5px
}

.card-btn {
    margin-top: 5px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.card-header {
    display: flex;
    justify-content: space-between;
}

.card-header-title {
    font-size: 13px;
    color: rgb(246, 104, 74)
}

.card-header-info {
    font-size: 10px;
    color: rgb(246, 104, 74)
}

.back-btn {
    display: flex;
    justify-content: start;
    align-items: center
}

.btn {
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}

.bottom-btn {
    margin-top: 10px;
    display: flex;
    justify-content: center;
}

.container-item-content {
    display: flex;
    flex-direction: column;
    justify-content: start;
    font-size: 10px
}

.container-item-content-text {
    margin: 5px;
}

.bottom-card {
    background-color: rgb(118, 124, 180);
}

.btn:active,
.btn:focus,
.btn:hover {
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}

.bottom-content {
    margin: 10px;
}

:deep(.el-card__body) {
    padding: 5px;
}

:deep(.el-card__header) {
    padding: 5px;
}

.result-bg {
    position: relative;
    height: 80vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #74ebd5, #acb6e5);
    animation: gradient-animation 5s ease infinite;
}

.share-btn {
    font-size: 20px;
    position: absolute;
    /* 绝对定位 */
    bottom: 10px;
    /* 距离底部10px */
    right: 10px;
    /* 距离右边10px */
    /* padding: 10px 15px; */
    /* background-color: #4CAF50; */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

@keyframes gradient-animation {
    0% {
        background: linear-gradient(135deg, #74ebd5, #acb6e5);
    }

    50% {
        background: linear-gradient(135deg, #acb6e5, #f64f59);
    }

    100% {
        background: linear-gradient(135deg, #74ebd5, #acb6e5);
    }
}
</style>