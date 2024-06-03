import { configureStore } from "@reduxjs/toolkit";
import { root } from "./root";
import storage from "redux-persist/lib/storage";
import {
  PERSIST,
  REHYDRATE,
  persistReducer,
  persistStore,
} from "redux-persist";
import { featureApiGenerator } from "./featureApiGenerator";

const persistConfig = {
  key: "root",
  storage,
  whitelist: ["auth"],
};
export const api = featureApiGenerator({ name: "api" });

const persistedReducer = persistReducer(persistConfig, root());

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: { ignoredActions: [REHYDRATE, PERSIST] },
    }).concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const persister = persistStore(store);
