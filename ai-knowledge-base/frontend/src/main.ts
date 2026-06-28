import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router/index";
import "./style.css";
import { useUserStore } from "./stores/user";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
const userStore = useUserStore(pinia);
userStore.restore();
if (userStore.token) {
  void userStore.fetchMe();
}
app.use(router);
app.mount("#app");
