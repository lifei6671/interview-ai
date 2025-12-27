import { ref } from 'vue'

export type PromptItem = {
  id: string
  title: string
  content: string
  tag: string
  views: number
  stars: number
  createdAt: string
  type: 'preset' | 'custom' | 'favorite'
}

const prompts = ref<PromptItem[]>([
  {
    id: 'p1',
    title: '英语考题设计',
    content: '你是一位资深英语老师，现在需要输出一套单词填空型考试试卷...',
    tag: '教育培训',
    views: 26670,
    stars: 391,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p2',
    title: '问题推导助手',
    content: '你是一个问题推导助手，需求提取题干、解析以及师生对话...',
    tag: '教育培训',
    views: 11581,
    stars: 148,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p3',
    title: '财务课程问题辅导',
    content: '你是一位资深的财务课程老师，需要以清晰步骤解释概念...',
    tag: '教育培训',
    views: 3390,
    stars: 78,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p4',
    title: '推导过程生成',
    content: '你是一名资深飞机机长，现在要完成飞行技术考试...',
    tag: '教育培训',
    views: 3322,
    stars: 39,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p5',
    title: '学习情况总结',
    content: '你是一个资深儿童教育老师，需要基于学生作业和表现...',
    tag: '教育培训',
    views: 3920,
    stars: 33,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p6',
    title: '作文点评',
    content: '你是一位资深小学语文老师，需要对学生作文做点评...',
    tag: '教育培训',
    views: 4340,
    stars: 59,
    createdAt: '2024-02-01 12:00:00',
    type: 'preset'
  },
  {
    id: 'p7',
    title: '照片写实2',
    content: '正向Prompt: Cherry Blossoms in Hokkaido in the winter time...',
    tag: '图像生成',
    views: 14654,
    stars: 182,
    createdAt: '2023-11-07 12:00:00',
    type: 'preset'
  },
  {
    id: 'p8',
    title: '3D角色',
    content: '正向Prompt: snowing winter, super cute baby pixar style...',
    tag: '图像生成',
    views: 8139,
    stars: 98,
    createdAt: '2023-11-07 12:00:00',
    type: 'preset'
  },
  {
    id: 'p9',
    title: '自定义模板示例',
    content: '为自定义业务场景生成结构化输出，包含步骤与关键字段...',
    tag: '自定义',
    views: 120,
    stars: 6,
    createdAt: '2024-05-09 09:30:00',
    type: 'custom'
  },
  {
    id: 'p10',
    title: '收藏模板示例',
    content: '面向收藏列表的模板内容展示...',
    tag: '收藏',
    views: 780,
    stars: 44,
    createdAt: '2024-03-12 18:20:00',
    type: 'favorite'
  }
])

const addPrompt = (item: PromptItem) => {
  prompts.value = [item, ...prompts.value]
}

export { prompts, addPrompt }
