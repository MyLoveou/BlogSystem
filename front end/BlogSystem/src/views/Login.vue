<template>
  <section class="login-wrapper">
    <!-- 遮罩层：与背景分离 -->
    <div class="mask" />

    <!-- 登录卡片 -->
    <el-card class="login-card">
      <template #header>
        <h2>星尘 · 登录</h2>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
        @keyup.enter="submit"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名 / 邮箱"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="submit"
          class="submit-btn"
        >
          登 录
        </el-button>
      </el-form>

    </el-card>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { login } from '@/apis/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const submit = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    const { detail, access_token, refresh_token } = await login(form)
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    ElMessage.success(detail)
    router.replace('/')
    localStorage.setItem('test','123')
  } catch (e) {
    console.error('登录失败', e)   // 建议保留，方便排查
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 主题变量 */
:root {
  --primary: #7a5af5;
  --secondary: #ff6b9c;
  --accent: #00d0ff;
  --dark: #0f0e17;
  --darker: #0a0a12;
  --light: #fffffe;
  --border-radius: 16px;
  --transition: all 0.3s ease;
}

.login-wrapper {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 禁止整页滚动 */
}

/* 半透明遮罩，与背景分离 */
.mask {
  position: absolute;
  inset: 0;
  background: rgba(10, 10, 18, 0);
  backdrop-filter: blur(4px);
}

/* 卡片：最大 90% 视口，内部滚动 */
.login-card {
  position: relative;
  width: 400px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  background: rgba(15, 14, 23, 0.75);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(122, 90, 245, 0.3);
  border-radius: var(--border-radius);
  box-shadow: 0 0 40px rgba(122, 90, 245, 0.25);
  overflow: hidden;
}

/* 卡片主体可滚动 */
:deep(.el-card__body) {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 24px 28px 20px;
}

.login-card h2 {
  text-align: center;
  color: var(--accent);
  margin: 0;
}

/* 表单 / 按钮保持原风格 */
.submit-btn {
  width: 100%;
  border: none;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  transition: var(--transition);
}
.submit-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 20px var(--primary);
}

.tip {
  margin-top: 12px;
  font-size: 0.875rem;
  text-align: center;
  color: var(--gray);
}
.tip a {
  color: var(--accent);
  text-decoration: none;
}
.tip a:hover {
  text-decoration: underline;
}
</style>