<template>
    <div class="usermanage">
        <div class="action_bar">
            <el-button type="primary" @click="dialogVisible=true">添加读者</el-button>
            <el-dialog
                v-model="dialogVisible"
                title="添加读者"
            >
                <el-form :model="form" ref="formRef" label-width="auto">
                    <el-form-item label="读者编号" prop="number">
                        <el-input v-model="form.number" placeholder="请输入读者编号" />
                    </el-form-item>
                    <el-form-item label="用户名" prop="user">
                        <el-input v-model="form.user" placeholder="请输入用户名" />
                    </el-form-item>
                    <el-form-item label="姓名" prop="name">
                        <el-input v-model="form.name" placeholder="请输入姓名" />
                    </el-form-item>
                    <el-form-item label="电话号码" prop="phone_number">
                        <el-input v-model="form.phone_number" placeholder="请输入电话号码" />
                    </el-form-item>
                    <el-form-item label="性别" prop="gender">
                        <el-input v-model="form.gender" placeholder="请输入性别" />
                    </el-form-item>
                    <el-form-item label="地址" prop="address">
                        <el-input v-model="form.address" placeholder="请输入地址" />
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitForm">确认添加</el-button>
                </template>
            </el-dialog>
            <el-button type="danger" @click="batchDelete">批量删除</el-button>
        </div>
        <el-table v-bind:data="data0" border style="width: 100%">
            <el-table-column prop="number" label="读者编号" />
            <el-table-column prop="user" label="用户名" />
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="phone_number" label="电话号码" />
            <el-table-column prop="gender" label="性别" />
            <el-table-column prop="address" label="地址" />
            <el-table-column prop="action" label="操作">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="openDeleteDialog(scope.row)">删除</el-button>

                </template>
            </el-table-column>
        </el-table>
        <el-pagination 
            background 
            layout="prev, pager, next" 
            :total="100" >
        </el-pagination>
    </div>
</template>

<script setup>
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';

onMounted(() => {
    axios.get('http://localhost:5000/api/reader')
        .then(response => {
            data0.value = response.data;
        })
        .catch(err => {
            ElMessage.error('获取读者信息失败');
            console.error(err);
        });
})
const data0 = ref([]);
const formRef = ref()

const form = ref({
    id: null,
    number: '',
    user: '',
    name: '',
    phone_number: '',
    gender: '',
    address: ''
});
const dialogVisible = ref(false);


function submitForm(){
    formRef.value.validate((valid) => {
        if (valid) {
            axios.post('http://localhost:5000/api/reader', form.value)
            .then(response => {
                ElMessage.success('添加成功');
                data0.value.push(response.data);
                dialogVisible.value = false;
                resetForm()
            })
            .catch(err => {
                ElMessage.error('添加失败')
                console.error(err)
            })

        } else {
            ElMessage.error('请填写完整信息');
        }
    });
}
function batchDelete() {
    // 这里可以添加批量删除的逻辑
    console.log("批量删除功能尚未实现");
}

function resetForm(){
    form.value = {
        id: null,
        user: '',
        name: '',
        phone_number: '',
        gender: '',
        address: ''
    }
}
</script>
<style scoped>
</style>