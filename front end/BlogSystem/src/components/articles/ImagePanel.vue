<template>
  <aside class="image-panel">
    <h4><i class="fas fa-images"></i> 图片仓库</h4>
    <el-upload :http-request="customUpload" :before-upload="beforeUpload" :on-success="onImgSuccess" multiple>
      <i class="fas fa-cloud-upload-alt" />
      <div class="tip">拖拽或点击上传</div>
    </el-upload>
    
    <!-- 显示元数据 -->
    <div class="metadata-display" v-if="metaData.categories.length || metaData.tags.length">
      <h5>分类</h5>
      <div class="tag-list">
        <el-tag v-for="cat in metaData.categories" :key="cat" size="small">{{ cat }}</el-tag>
      </div>
      <h5>标签</h5>
      <div class="tag-list">
        <el-tag v-for="tag in metaData.tags" :key="tag" type="info" size="small">{{ tag }}</el-tag>
      </div>
    </div>

    <!-- 图片列表 -->
    <ul class="img-list">
      <li v-for="img in imageList" :key="img.image">
        <img :src="img.image" />
        <span>{{ img.name }}</span>
        <button @click="copy(img.image)"><i class="fas fa-copy"></i></button>
        <button @click="deleteImage(img.id)"><i class="fas fa-trash"></i></button>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { ElMessage } from 'element-plus'

defineProps({
  metaData: Object,
  imageList: Array,
  customUpload: Function,
  beforeUpload: Function,
  onImgSuccess: Function,
  deleteImage: Function
});

const copy = (url) => {
  navigator.clipboard.writeText(url);
  ElMessage.success('已复制');
};
</script>

<style scoped>
.image-panel {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(122, 90, 245, 0.2);
  border-left: none;
  border-radius: 0 0 var(--border-radius) 0;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 200px;
  overflow-y: auto;
}

.image-panel h4 {
  color: var(--accent);
  font-size: 1rem;
  margin: 0;
}

.uploader {
  border: 2px dashed var(--primary);
  border-radius: 8px;
  padding: 20px 5px;
  text-align: center;
  color: var(--gray);
}

.uploader:hover {
  border-color: var(--accent);
}

.metadata-display {
  margin: 15px 0;
  padding: 10px;
  background: rgba(122, 90, 245, 0.1);
  border-radius: 8px;
}

.metadata-display h5 {
  margin: 5px 0;
  color: var(--accent);
  font-size: 0.85rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}

.tag-list .el-tag {
  margin: 2px;
}

.img-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.img-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.img-list img {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 6px;
}

.img-list span {
  flex: 1;
  font-size: 0.75rem;
  color: var(--light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.img-list button {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
}
</style>