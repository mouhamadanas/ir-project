import axios from "axios";
import { store } from "src/reduxConfig/store";

export const authAxios = axios.create();

authAxios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    ///catch all errors from here
    return error;
  }
);

//add your headers here
authAxios.interceptors.request.use((config: any) => {
  config.headers["Authorization"] = `Bearer ${store.getState().auth.token} `;
  return config;
});
