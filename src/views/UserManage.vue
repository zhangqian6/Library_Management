<template>
    <div class="usermanage">
        <div class="batch_del">
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
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
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
function batchDelete() {
    // 这里可以添加批量删除的逻辑
    console.log("批量删除功能尚未实现");
}
</script>
<style scoped>
</style>