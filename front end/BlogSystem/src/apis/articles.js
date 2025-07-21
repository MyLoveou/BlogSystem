import request from '@/utils/request'

// 文章 API
export const postArticle = (article) => {
  console.log(article)
  return request.post('/articles/', article)
};

export const getCategoryList = () => {
  console.log("获取分类列表")
  return request.get('/categories/')
}

export const getTagList = () => {
  return request.get('/tags')
}

export const createCategory = (category) => {
  console.log(category)
  return request.post('/categories/',{"name": category })
} 

export const createTag = (tag) => {
  return request.post('/tags/', {"name": tag })
}

export const getArticleList = (params) => {
  console.log(params, "测试")
  return request.get('/articles/', { params })
}