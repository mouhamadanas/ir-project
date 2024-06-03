import { createSlice } from "@reduxjs/toolkit";
type propsType = {
  token?: string;
  user?: {};
};
const initialState: propsType = {
  token: "",
  user: {},
};

const authSlice = createSlice({
  name: "test",
  initialState,
  reducers: {
    resetAuthData: (state) => {
      state.token = undefined;
      state.user = undefined;
    },
    setLoginData: (state, action) => {
      state.token = action.payload.token;
      state.user = action.payload.user;
    },
  },
});
export const { resetAuthData, setLoginData } = authSlice.actions;
export default authSlice.reducer;
