// src/composables/useImageUpload.js
import { ref } from 'vue'
import request from '@/utils/request'
import { ElMessage, ElMessageBox } from 'element-plus'

export default function useImageUpload() {
  const imageList = ref([])

  /* ----------------- 自定义上传 ----------------- */
  const customUpload = async ({ file, onError }) => { // 移除 onSuccess 参数
    const formData = new FormData()
    formData.append('image', file)

    try {
      const res = await request.post('/images/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      // 注意：此处不再调用 onSuccess(res)
      return res // 返回结果供 el-upload 内部使用
    } catch (e) {
      onError(e)
      throw e // 抛出错误确保 el-upload 能捕获
    }
  }
  /* ----------------- 业务回调 ----------------- */
  const onImgSuccess = (res) => {
    imageList.value.unshift(res)
    console.log(imageList.value)
    return res.image
  }

  const beforeUpload = (file) => {
    const isImg = file.type.startsWith('image/')
    const isLt2M = file.size / 1024 / 1024 < 2
    if (!isImg) ElMessage.error('必须是图片')
    if (!isLt2M) ElMessage.error('图片不能超过 2MB')
    return isImg && isLt2M
  }
    /* ----------------- 删除 ----------------- */
  const deleteImage = async (id) => {
    await ElMessageBox.confirm('确定删除这张图片？', '提示', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })

    try {
      const res = await request.delete(`/images/${id}/`)
      // imageList.value = imageList.value.filter(item => item.id !== id)
      fetchImages()
      ElMessage.success(res.detail)
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }

  /* ----------------- 获取图片列表 ----------------- */
  const fetchImages = async () => {
    const data = await request.get('/images/')
    imageList.value = data
  }

  /* ----------------- 导出 ----------------- */
  return {
    imageList,
    deleteImage,    // 供 <el-image> 调用
    customUpload,   // 供 <el-upload :http-request="customUpload">
    onImgSuccess,   // 供 <el-upload @success="onImgSuccess">
    beforeUpload,   // 供 <el-upload :before-upload="beforeUpload">
    fetchImages
  }
}