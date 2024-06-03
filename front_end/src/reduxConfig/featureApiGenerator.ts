import { BaseQueryFn, createApi } from "@reduxjs/toolkit/query/react";
import { authAxios } from "src/config/axios";
import { AxiosRequestConfig, AxiosError } from "axios";
import { settings } from "src/config/settings";
import { baseUrl } from "src/env/baseUrl";
const errorsCode = ["ERR_BAD_RESPONSE", "ERR_NETWORK", "ERR_BAD_REQUEST"];
//parameter types
type propsType = {
  name: string;
};

/// the axios configuration for RTk query
const axiosBaseQuery =
  ({
    baseUrl,
  }: {
    baseUrl: string;
  }): BaseQueryFn<
    {
      url: string;
      method?:
        | (AxiosRequestConfig["method"] & "POST")
        | "PATCH"
        | "DELETE"
        | "GET"
        | "PUT";
      data?: AxiosRequestConfig["data"];
      params?: AxiosRequestConfig["params"];
    },
    unknown,
    unknown
  > =>
  async ({ url, method, data, params }) => {
    // try {
    const result = await authAxios({
      url: baseUrl + url,
      method,
      data,
      params,
    })
      .then((res) => res)
      .catch((err) => {
        return { error: err };
      });

    if ((result as any).name === "AxiosError")
      return {
        error: result,
      };
    else return result;
  };

// the api generator
export const featureApiGenerator = ({ name }: propsType) => {
  const api = createApi({
    reducerPath: name,
    baseQuery: axiosBaseQuery({
      baseUrl: baseUrl,
    }),

    keepUnusedDataFor: settings.staleDataBeforeReFetching,
    endpoints: () => ({}),
  });
  return api;
};
