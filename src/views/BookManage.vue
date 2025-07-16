<template>
    <div class="book-manage">
        <el-dialog v-model="dialogVisible2">
            <span>确定要删除这本图书吗？</span>
            <template #footer>
                <el-button @click="dialogVisible2=false">取消</el-button>
                <el-button @click="handleDelete" style="background-color: red;">确定</el-button>
            </template>
        </el-dialog>

        <div class="search-bar">
            <div class="search-item">
                <label class="label">图书编号</label>
                <el-input  v-model="book_num" placeholder="请输入图书编号" clearable/>
            </div>
            <div class="search-item">
                <label class="label">图书名称</label>
                <el-input  v-model="book_name" placeholder="请输入图书名称" clearable/>
            </div>
            <div class="search-item">
                <label class="label">作者</label>
                <el-input  v-model="book_author" placeholder="请输入作者" clearable/>
            </div>
            <el-button type="primary" @click="query_books">查询</el-button>
            <el-button type="primary" style="background-color: red" @click="query_reset">重置</el-button>
        </div>
        <div class="action-bar">
            <el-button type="primary" @click="dialogVisible = true">上架</el-button>
            <el-dialog :title="isEditMode? '修改书籍信息' : '上架新书籍'" v-model="dialogVisible">
                <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
                    <el-form-item label="图书编号" prop="number">
                        <el-input v-model="form.number" placeholder="请输入图书编号"/>
                    </el-form-item>
                    <el-form-item label="书名" prop="title">
                        <el-input v-model="form.title" placeholder="请输入书名"/>
                    </el-form-item>
                    <el-form-item label="作者" prop="author">
                        <el-input v-model="form.author" placeholder="请输入作者名"/>
                    </el-form-item>
                    <el-form-item label="价格" prop="price">
                        <el-input v-model="form.price" placeholder="请输入价格"/>
                    </el-form-item>
                    <el-form-item label="出版社" prop="publish">
                        <el-input v-model="form.publish" placeholder="请输入出版社"/>
                    </el-form-item>
                    <el-form-item label="出版时间" prop="publishDate">
                        <el-input v-model="form.publishDate" placeholder="请输入出版时间"/>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitForm">确认上架</el-button>
                </template>
            </el-dialog>
            <el-button type="primary" style="background-color: red" @click="deleteMore">批量删除</el-button>
        </div>



        <el-table v-bind:data="pagedData" stripe @selection-change="handleSelectionChange" style="width: 100%">
            <el-table-column type="selection" width="55" />
            <el-table-column prop="number" label="图书编号" />
            <el-table-column prop="title" label="图书名称" />
            <el-table-column prop="author" label="作者" />
            <el-table-column prop="price" label="价格" />
            <el-table-column prop="publish" label="出版社" />
            <el-table-column prop="publishDate" label="出版时间" />
            <el-table-column prop="status" label="状态" >
                <template #default="scope">
                    <el-tag :type="scope.row.status === '已借阅' ? 'success' : 'warning'">
                        {{ scope.row.status }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="action" label="操作">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
                    <el-button type="danger" size="small" @click="openDeleteDialog(scope.row)">删除</el-button>

                </template>
            </el-table-column>
            
        </el-table>
        <el-pagination
            v-model:current-page="currentPage1"
            size="large"
            :page-size="pageSize"
            :disabled="false"
            :background="true"
            layout="prev, pager, next"
            :total="tableData?.length || 0"
            @current-change="updatePagedData"
        />

        <!-- <div class="book-list">
            <el-table :data="books" style="width: 100%">
                <el-table-column prop="title" label="书名" />
            </el-table>
        </div> -->
    </div>
</template>
<script setup>
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';

// 分页操作
const pageSize = ref(10)
const currentPage1 = ref(1)
const pagedData = ref()
const formRef = ref()
const tableData = ref()

// 批量删除数据
const multipleSelection = ref([])

// 用于查询重置
const book_num = ref('')
const book_name = ref('')
const book_author = ref('')

const dialogVisible = ref(false)
const dialogVisible2 = ref(false)
const editingIndex = ref(null)
const isEditMode = ref(false)
const selectedRow = ref(null)
onMounted(() => {
    axios.get('http://localhost:5000/api/books')
    .then(res => {
        console.log('后端返回数据', res.data)
        tableData.value = res.data
    })
})
watch(tableData, () =>{
    updatePagedData()
})
const form = ref({
    id: null,
    number: '',
    title: '',
    author: '',
    price: '',
    publish: '',
    publishDate: '',
    status:'未借阅'
})
const rules = {
    number: [{required: true, message: '请输入图书编号', trigger: 'blur'}],
    title: [{required: true, message: '请输入图书名称', trigger: 'blur'}],
    author: [{required: true, message: '请输入作者', trigger: 'blur'}],
    price: [{required: true, message: '请输入价格', trigger: 'blur'}],
    publish: [{required: true, message: '请输入出版社', trigger: 'blur'}],
    publishDate: [{required: true, message: '请输入出版时间', trigger: 'blur'}],
}


function submitForm(){
    formRef.value.validate(valid => {
        if(valid){
            if(isEditMode.value){
                const id = form.value.id
                axios.put(`http://localhost:5000/api/books/${id}`, form.value)
                    .then(res => {
                        //编辑操作，更新原有数据
                        tableData.value[editingIndex.value] = {...form.value}
                        updatePagedData()
                        ElMessage.success('修改成功！')
                        dialogVisible.value = false
                        resetForm()
                    })
                    .catch(err => {
                        ElMessage.error('修改失败')
                        console.error(err)
                    })
                
            }else{
                axios.post('http://localhost:5000/api/books', form.value)
                    .then(res => {
                        ElMessage.success('新书籍上架成功')
                        tableData.value.push(res.data)
                        updatePagedData()
                        dialogVisible.value = false
                        resetForm()
                    })
                    .catch(err => {
                        ElMessage.error('添加失败')
                        console.error(err)
                    })
            }
        }else{
            ElMessage.error('请完整填写表单信息')
        }
    })
}

function handleEdit(row){
    const index = tableData.value.findIndex(item => item === row)
    console.log('index',index)

    //保存索引
    editingIndex.value = index
    form.value = {...row}

    isEditMode.value = true
    //打开弹窗
    dialogVisible.value = true
}

function openDeleteDialog(row){
    dialogVisible2.value = true
    selectedRow.value = row
}

//删除书籍
function handleDelete(){
    const bookId = selectedRow.value.id
    if(!bookId){
        ElMessage.error('未找到图书ID, 无法删除')
        return
    }
    //调用后端接口删除书籍信息
    axios.delete(`http://localhost:5000/api/books/${bookId}`)
        .then(res => {
            ElMessage.success('删除成功')
            // 从tableData中移除已删除项
            const index = tableData.value.findIndex(item => item.id === bookId)
            if (index !== -1){
                tableData.value.splice(index, 1)
                updatePagedData()
            }
            dialogVisible2.value = false
        })
        .catch(err => {
            ElMessage.error('删除失败, 请稍后再试')
            console.error(err)
        })

    
}

// 批量删除
function handleSelectionChange(val){
    multipleSelection.value = val
}
function deleteMore(){
    if(multipleSelection.value.length === 0){
        ElMessage.warning('请先选择要删除的图书')
        return
    }
    ElMessageBox.confirm(
        '确定要删除选中的图书吗？',
        '提示',
        {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }
    ).then(() => {
        // 用户确认删除
        const bookId = multipleSelection.value.map(item => item.id)
        if(!bookId){
            ElMessage.error('未找到图书ID, 无法删除')
            return
        }
        axios.delete(`http://localhost:5000/api/books/${bookId.join(',')}`)
        .then(res => {
            ElMessage.success('删除成功')
            // 从tableData中移除已删除项
            multipleSelection.value.forEach(item => {
                const index = tableData.value.findIndex(book => book.id === item.id)
                if (index !== -1){
                    tableData.value.splice(index, 1)
                    updatePagedData()
                }
            })
            dialogVisible2.value = false
        })
        .catch(err => {
            ElMessage.error('删除失败, 请稍后再试')
            console.error(err)
        })
    }).catch(() => {
        // 用户取消删除
        ElMessage.info('已取消删除操作')
    })
    

}

function resetForm(){
    form.value = {
        number: '',
        title: '',
        author: '',
        price: '',
        publish: '',
        publishDate: '',
        status: '未借阅'
    }
    isEditMode.value = false
}

function updatePagedData(){
    console.log(currentPage1.value)
    const start = (currentPage1.value - 1) * pageSize.value
    const end = start + pageSize.value
    pagedData.value = tableData.value?.slice(start, end) || []
    console.log('单页数据为', pagedData.value)
}

function query_reset(){
    // 重置查询条件
    book_num.value = ''
    book_author.value = ''
    book_name.value = ''
}

function query_books(){
    // 根据查询条件过滤数据
    const filteredData = tableData.value.filter(book => {
        return (!book_num.value || book.number === book_num.value) &&
               (!book_name.value || book.title === book_name.value) &&
               (!book_author.value || book.author === book_author.value);
    });
    pagedData.value = filteredData.slice(0, pageSize.value);
    currentPage1.value = 1; // 重置到第一页
}

</script>
<style scoped>
.book-manage{
    padding: 20px;
    width: 100%;
    height: 100%;
}
.search-bar{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.search-bar el-input{
    width: 200px;
}
.search-item{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
}

.search-item .label{
    white-space: nowrap;
    font-size: 14px;
}
.action-bar{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
    margin-top: 30px;
    margin-bottom: 20px;
}
</style>