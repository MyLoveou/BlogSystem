<template>
  <el-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue')" title="编辑文章元数据" width="500px">
    <el-form label-width="80px">
      <el-form-item label="分类">
        <el-select v-model="localCats" multiple filterable allow-create default-first-option placeholder="输入分类" style="width:100%"/>
      </el-form-item>
      <el-form-item label="标签">
        <el-select v-model="localTags" multiple filterable allow-create default-first-option placeholder="输入标签" style="width:100%"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps(['modelValue', 'categories', 'tags'])
const emit  = defineEmits(['update:modelValue', 'save'])

const localCats = computed({ get: () => props.categories, set: val => emit('save', { cats: val, tags: props.tags }) })
const localTags = computed({ get: () => props.tags,   set: val => emit('save', { cats: props.categories, tags: val }) })
</script>