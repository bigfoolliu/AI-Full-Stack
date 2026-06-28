/// <reference types="vite/client" />

// 给 TypeScript 看的 .vue 模块声明文件
// 解决 TS 无法识别 .vue 文件
// TypeScript 原生只识别 .ts/.js，直接 import Login from './Login.vue' 会报模块找不到的类型错误；这段代码做模块声明，让 TS 认可 vue 文件合法。
// / <reference types="vite/client" />
// 加载 Vite 官方类型：提供 import.meta.env 环境变量、import.meta.glob、Vite 内置全局变量的 TypeScript 语法提示，否则写环境变量会飘红。
declare module "*.vue" {
  import type { DefineComponent } from "vue";

  const component: DefineComponent<{}, {}, any>;
  export default component;
}
