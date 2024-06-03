import { api } from "src/reduxConfig/store";
import { endPoints } from "src/shared/endPoints";

export type resType = {
  id: string;
  name: string;
};

const testService = api.injectEndpoints({
  endpoints: (build) => {
    return {
      getTest: build.query<resType, string>({
        query: (id) => ({ url: `${endPoints.testEndPoint}/${id}` }),
      }),
    };
  },
});

export const { useGetTestQuery } = testService;
