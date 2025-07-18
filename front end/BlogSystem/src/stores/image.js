import { ref } from 'vue'
import { useImageUpload } from '@/apis/useImageUpload'

export function useImageStore() {
  const { imageList: images, customUpload, onImgSuccess, beforeUpload, fetchImages, deleteImage } = useImageUpload()
  return { images, upload: customUpload, before: beforeUpload, remove: deleteImage }
}