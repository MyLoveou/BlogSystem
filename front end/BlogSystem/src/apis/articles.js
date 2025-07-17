import request from '@/utils/request'

// 文章 API
export const postArticle = (article) => {
  return request.post('/articles/', article);
};