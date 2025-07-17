<template>
  <el-dialog v-model="showMetaDialog" title="编辑文章元数据" width="500px">
    <el-form label-width="80px">
      <el-form-item label="分类">
        <el-select
          v-model="metaData.categories"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入分类"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="标签">
        <el-select
          v-model="metaData.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入标签"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:showMetaDialog', false)">取消</el-button>
      <el-button type="primary" @click="$emit('save')">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
defineProps({
  showMetaDialog: Boolean,
  metaData: Object
});

defineEmits(['update:showMetaDialog', 'save']);
</script>