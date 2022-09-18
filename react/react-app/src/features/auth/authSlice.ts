import axios from "axios";
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { PROPS_AUTHEN } from "../types";
import { RootState } from "../../app/store";

export const getSession = createAsyncThunk("/auth/session", async () => {
  console.log("getSession");
  const res = await axios.get("/accounts/session/");
  console.log(res.status);

  if (res.data.isAuthenticated) {
    return true;
  } else {
    return false;
  }
});

export const getCSRF = createAsyncThunk("/auth/csrf", async () => {
  console.log("getCSRF");
  const res = await axios.get("/accounts/csrf/");
  console.log(res.status);

  return res.headers["x-csrftoken"];
});

export const fetchAsyncLogin = createAsyncThunk(
  "/auth/login",
  async (authen: PROPS_AUTHEN) => {
    console.log("fetchAsyncLogin");
    const res = await axios.post("/accounts/login/", authen.input, {
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": authen.csrfToken,
      },
    });
    console.log(res.status);

    return res.status;
  }
);

export const fetchAsyncLogout = createAsyncThunk("/auth/logout", async () => {
  console.log("fetchAsyncLogout");
  const res = await axios.get("/accounts/logout/");
  console.log(res.status);

  return res.status;
});

export const whoami = createAsyncThunk("/auth/whoami", async () => {
  console.log("whoami");
  const res = await axios.get("/accounts/whoami/", {
    headers: {
      "Content-Type": "application/json",
    },
  });
  console.log(res.status);

  return res.data;
});

export const authSlice = createSlice({
  name: "auth",
  initialState: {
    openSignIn: true,
    openSignUp: false,
    openProfile: false,
    isLoadingAuth: false,
    myprofile: {
      username: "",
    },
    csrf: "",
    isAuthenticated: false,
  },
  reducers: {
    fetchCredStart(state) {
      state.isLoadingAuth = true;
    },
    fetchCredEnd(state) {
      state.isLoadingAuth = false;
    },
    setOpenSignIn(state) {
      state.openSignIn = true;
    },
    resetOpenSignIn(state) {
      state.openSignIn = false;
    },
    setOpenSignUp(state) {
      state.openSignUp = true;
    },
    resetOpenSignUp(state) {
      state.openSignUp = false;
    },
    setOpenProfile(state) {
      state.openProfile = true;
    },
    resetOpenProfile(state) {
      state.openProfile = false;
    },
    setCsrf(state, action) {
      state.csrf = action.payload;
    },
    resetCsrf(state) {
      state.csrf = "";
    },
    setIsAuthenticated(state) {
      state.isAuthenticated = true;
    },
    resetIsAuthenticated(state) {
      state.isAuthenticated = false;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getSession.fulfilled, (state, action) => {
      console.log("getSessionExtraReducer");
      state.isAuthenticated = action.payload;
      console.log(state.isAuthenticated);
    });
    builder.addCase(getCSRF.fulfilled, (state, action) => {
      console.log("getCsrfExtraReducer");
      state.csrf = action.payload;
      console.log(state.csrf);
    });
    builder.addCase(fetchAsyncLogin.fulfilled, (state, action) => {
      console.log("fetchAsyncLoginExtraReducer");
      state.isAuthenticated = true;
    });
    builder.addCase(fetchAsyncLogout.fulfilled, (state, action) => {
      console.log("fetchAsyncLogoutExtraReducer");
      state.isAuthenticated = false;
      state.openSignIn = true;
    });
    builder.addCase(whoami.fulfilled, (state, action) => {
      console.log("whoamiExtraReducer");
      console.log(action.payload.username);
    });
  },
});

export const {
  fetchCredStart,
  fetchCredEnd,
  setOpenProfile,
  setOpenSignIn,
  setOpenSignUp,
  resetOpenProfile,
  resetOpenSignIn,
  resetOpenSignUp,
  setCsrf,
  resetCsrf,
  setIsAuthenticated,
  resetIsAuthenticated,
} = authSlice.actions;

export const selectIsLoadingAuth = (state: RootState) =>
  state.auth.isLoadingAuth;
export const selectOpenSignIn = (state: RootState) => state.auth.openSignIn;
export const selectOpenSignUp = (state: RootState) => state.auth.openSignUp;
export const selectOpenProfile = (state: RootState) => state.auth.openProfile;
export const selectMyprofile = (state: RootState) => state.auth.myprofile;
export const selectCsrf = (state: RootState) => state.auth.csrf;
export const selectIsAuthenticated = (state: RootState) =>
  state.auth.isAuthenticated;

export default authSlice.reducer;
