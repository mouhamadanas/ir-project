import { api } from "src/reduxConfig/store";
import { endPoints } from "src/shared/endPoints";

export type resType = {
  id: string;
  name: string;
};

const testService = api.injectEndpoints({
  endpoints: (build) => {
    return {
      getSuggest: build.mutation({
        query: ({ query, data }) => ({
          url: `${endPoints.suggestionEndpoint}?data=${data}`,
          method: "POST",
          data: { query },
        }),
      }),
      getResultWithCluster: build.mutation({
        query: ({ query, data }) => ({
          url: `${endPoints.queryWithCluster}?data=${data}`,
          method: "POST",
          data: { query },
        }),
      }),
      getResultWithoutCluster: build.mutation({
        query: ({ query, data }) => ({
          url: `${endPoints.queryWithOutCluster}?data=${data}`,
          method: "POST",
          data: { query },
        }),
      }),
    };
  },
});

export const {
  useGetSuggestMutation,
  useGetResultWithClusterMutation,
  useGetResultWithoutClusterMutation,
} = testService;
