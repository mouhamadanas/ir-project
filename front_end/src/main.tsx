import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { Provider } from "react-redux";
import { persister, store } from "./reduxConfig/store";
import { PersistGate } from "redux-persist/integration/react";
import { ThemeProvider } from "@emotion/react";
import { theme } from "./theme";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import I18nextBrowserLanguageDetector from "i18next-browser-languagedetector";
import I18NextHttpBackend from "i18next-http-backend";
import { CssBaseline } from "@mui/material";
import { settings } from "./config/settings";

import "src/assets/globalStyle.scss";

i18next
  .use(initReactI18next)
  .use(I18nextBrowserLanguageDetector)
  .use(I18NextHttpBackend)
  .init({
    fallbackLng: settings.defaultLanguage,
    debug: false,
    detection: {
      order: ["cookie"],
      caches: ["cookie"],
    },
  });

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={<>loading...</>} persistor={persister}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </PersistGate>
    </Provider>
  </React.StrictMode>
);
