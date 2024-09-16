<template>
    <div class="rank" v-loading="loading">
        <div class="table">
            <el-button class="btn" @click="showAdd" style="margin-bottom: 10px;">添加成绩</el-button>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column type="index" label="排名" width="80" />
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="avg_score" label="平均分"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button @click="showDel(scope.row.id)" size="small" text type="danger">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>


        <el-dialog v-model="addDialogFormVisible" title="添加成绩" width="90%">
            <el-form :model="addForm">
                <el-form-item label="用户名" :label-width="labelWidth" style="margin-right: 19px;">
                    <el-input v-model="addForm.username" autocomplete="off" />
                </el-form-item>
                <div v-for="(semesterItem, semesterIdx) in addForm.semester_children" :key="semesterIdx">
                    <el-form-item label="学期" :label-width="labelWidth">
                        <div class="course-item">
                            <el-input v-model="semesterItem.semester_title" autocomplete="off" />
                            <el-icon style="margin-left: 5px; color: blue" @click="addSemesterItem">
                                <CirclePlusFilled />
                            </el-icon>
                        </div>
                    </el-form-item>
                    <div style="margin-left: 30px" v-for="(courseItem, courseIdx) in semesterItem.course_children">
                        <el-form-item label="课程" :label-width="labelWidth" :key="courseIdx">
                            <div class="course-item">
                                <el-input v-model="courseItem.course_title" autocomplete="off" />
                                <el-icon style="margin-left: 5px; color: blue"
                                    @click="addCourseItem(semesterIdx, courseIdx)">
                                    <CirclePlusFilled />
                                </el-icon>
                            </div>
                        </el-form-item>
                        <el-form-item label="分数" :label-width="labelWidth" :key="courseIdx" style="margin-right: 19px;">
                            <el-input v-model="courseItem.score" autocomplete="off" type="number" />
                        </el-form-item>
                    </div>
                </div>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="addDialogFormVisible = false">取消</el-button>
                    <el-button class="btn" @click="showSubmit">
                        保存
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <el-dialog v-model="resultDialogFormVisible" width="90%">
            <div class="result-bg" ref="screenshotArea">
                <div style="margin: 10px">
                    <h3>恭喜您：{{ addForm.username }}，您使用的GPA⼯具，结果显示打败了{{ result }}%的华人</h3>
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
import html2canvas from "html2canvas";

const loading = ref(false)
const tableData = ref([])
const addDialogFormVisible = ref(false)
const resultDialogFormVisible = ref(false)

const addForm = reactive({
    username: "",
    semester_children: [{
        "semester_title": "",
        "course_children":
            [{
                "course_title": "",
                "score": ""
            }]
    }]
})

const labelWidth = ref(60)

const fetchRankData = async () => {

    try {
        loading.value = true
        const response = await axios.post('/api/rank/v1/list')
        tableData.value = response.data.data
    } catch (error) {
        console.error('Failed to fetch rank data:', error)
    } finally {
        loading.value = false
    }
}

const del = async (id) => {
    try {
        const response = await axios.post('/api/rank/v1/del', {
            "id": id
        })
        tableData.value = response.data.data
    } catch (error) {
        console.error(error)
    }
}

const addSemesterItem = () => {
    addForm.semester_children.push({
        "semester_title": "",
        "course_children":
            [{
                "course_title": "",
                "score": ""
            }]
    })
}

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

const addCourseItem = (semesterIdx, courseIdx) => {
    addForm.semester_children[semesterIdx].course_children.push({
        "course_title": "",
        "score": ""
    })
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
                fetchRankData()
            })
        })
}

const saveRank = async () => {
    try {
        const response = await axios.post('/api/rank/v1/add', addForm)
        return response

    } catch (error) {
        console.error('Failed to fetch rank data:', error)
    }
}

const showSubmit = async () => {

    ElMessageBox.confirm(
        '确定提交?',
        '提示',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    )
        .then(() => {
            saveRank().then(res => {
                if (res.data.code === 0) {
                    result.value = res.data.data
                    resultDialogFormVisible.value = true

                    fetchRankData()
                } else {
                    ElMessage({
                        type: 'error',
                        message: res.data.msg,
                    })
                }

            })
        })
}

const showAdd = async () => {
    addDialogFormVisible.value = true
}

const result = ref("")

onMounted(() => {
    fetchRankData()
})

</script>

<style scoped>
.rank {
    flex: 1;
    padding: 20px 20px 40px 20px;
    /* text-align: center; */
}

.course-item {
    display: flex;
    align-items: center;
    width: 100%;
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

.btn {
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}

.btn:active,
.btn:focus,
.btn:hover {
    /* 禁用按钮点击后的颜色变化 */
    background-color: rgb(246, 104, 74);
    color: aliceblue;
}
</style>