import { combineReducers } from "@reduxjs/toolkit";
import authReducer from "src/app/login/services/slice";
import { api } from "./store";

/// you need to add every slice reducer you created here
export const root = () => {
  return combineReducers({
    [api.reducerPath]: api.reducer,
    auth: authReducer,
  });
};
