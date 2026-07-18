import { ElMessage, ElNotification } from 'element-plus'

export function toastSuccess(msg: string) {
  ElMessage.success(msg)
}

export function toastError(msg: string) {
  ElMessage.error(msg)
}

export function toastWarning(msg: string) {
  ElMessage.warning(msg)
}

export function toastInfo(msg: string) {
  ElMessage.info(msg)
}

export function notifySuccess(title: string, message?: string) {
  ElNotification({ title, message, type: 'success' })
}

export function notifyError(title: string, message?: string) {
  ElNotification({ title, message, type: 'error' })
}
