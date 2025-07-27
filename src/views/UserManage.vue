<template>
    <div class="usermanage">
        <div class="action_bar">
            <el-button type="primary" @click="dialogVisible=true">添加读者</el-button>
            <el-dialog
                v-model="dialogVisible"
                title="添加读者"
            >
                <el-form :model="form" label-width="auto">
                    <el-form-item label="读者编号" prop="id">
                        <el-input v-model="form.id" placeholder="请输入读者编号" />
                    </el-form-item>
                    <el-form-item label="用户名" prop="id">
                        <el-input v-model="form.id" placeholder="请输入用户名" />
                    </el-form-item>
                    <el-form-item label="姓名" prop="id">
                        <el-input v-model="form.id" placeholder="请输入姓名" />
                    </el-form-item>
                    <el-form-item label="电话号码" prop="id">
                        <el-input v-model="form.id" placeholder="请输入电话号码" />
                    </el-form-item>
                    <el-form-item label="性别" prop="id">
                        <el-input v-model="form.id" placeholder="请输入性别" />
                    </el-form-item>
                    <el-form-item label="地址" prop="id">
                        <el-input v-model="form.id" placeholder="请输入地址" />
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitForm">确认添加</el-button>
                </template>
            </el-dialog>
            <el-button type="danger" @click="batchDelete">批量删除</el-button>
        </div>
        <el-table :data="[]" border style="width: 100%">
            <el-table-column prop="id" label="读者编号" />
            <el-table-column prop="name" label="用户名" />
            <el-table-column prop="email" label="姓名" />
            <el-table-column prop="role" label="电话号码" />
            <el-table-column prop="status" label="性别" />
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

const form = ref({
    id: '',
    user: '',
    name: '',
    phone_number: '',
    gender: '',
    address: ''
});
const dialogVisible = ref(false);


function submitForm(){
    console.log("添加读者功能尚未实现");
}
function batchDelete() {
    // 这里可以添加批量删除的逻辑
    console.log("批量删除功能尚未实现");
}
</script>
<style scoped>
</style>