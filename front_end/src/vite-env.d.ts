/// <reference types="vite/client" />
declare module "*.module.scss";

declare module "*.jpg";
declare module "*.json";
declare module "*.png";
declare module "*.svg";

declare namespace React {
  function lazy<T extends ComponentType<any>>(
    factory: () => Promise<{ default: T }>
  ): T;
}
