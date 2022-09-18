import React from 'react';
import { AppDispatch } from '../../app/store';
import { useSelector, useDispatch } from 'react-redux';
import styles from './Auth.module.css';
import Modal from 'react-modal';
import { Formik } from 'formik';
import { TextField, Button, CircularProgress } from '@mui/material';
import {
  selectIsLoadingAuth,
  selectOpenSignIn,
  fetchCredStart,
  fetchCredEnd,
  setOpenSignUp,
  resetOpenSignIn,
  fetchAsyncLogin,
  selectCsrf,
  selectIsAuthenticated
} from './authSlice';

const customStyles = {
  overlay: {
    backgroundColor: "#777777",
  },
  content: {
    top: "55%",
    left: "50%",

    width: 500,
    height: 700,
    padding: "50px",

    transform: "translate(-50%, -50%)",
  },
};

const Auth: React.FC = () => {
  Modal.setAppElement("#root");
  const openSignIn = useSelector(selectOpenSignIn);
  const isLoadingAuth = useSelector(selectIsLoadingAuth);
  const csrfToken = useSelector(selectCsrf);
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const dispatch: AppDispatch = useDispatch();

  return (
    <div>
      <Modal
        isOpen={openSignIn}
        onRequestClose={async () => {
          if (isAuthenticated){
            dispatch(resetOpenSignIn());
          }
        }}
        style={customStyles}
      >
        <Formik
          initialErrors={{ username: "required" }}
          initialValues={{ username: "", password: "" }}
          onSubmit={async (values) => {
            dispatch(fetchCredStart());
            
            const result = await dispatch(fetchAsyncLogin({input: values, csrfToken: csrfToken}));
            
            if (fetchAsyncLogin.fulfilled.match(result)) {
              //await dispatch(fetchAsyncGetProfs());
              //await dispatch(fetchAsyncGetPosts());
              //await dispatch(fetchAsyncGetComments());
              //await dispatch(fetchAsyncGetMyProf());
            }
            
            dispatch(fetchCredEnd());

            if (isAuthenticated){
              dispatch(resetOpenSignIn());
            }
          }}
        >
          {({
            handleSubmit,
            handleChange,
            handleBlur,
            values,
            errors,
            touched,
            isValid,
          }) => (
            <div>
              <form onSubmit={handleSubmit}>
                <div className={styles.auth_signUp}>
                  <h1 className={styles.auth_title}>SNS clone</h1>
                  <br />
                  <div className={styles.auth_progress}>
                    {isLoadingAuth && <CircularProgress />}
                  </div>
                  <br />

                  <TextField
                    placeholder="username"
                    type="input"
                    name="username"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.username}
                  />

                  {touched.username && errors.username ? (
                    <div className={styles.auth_error}>{errors.username}</div>
                  ) : null}
                  <br />

                  <TextField
                    placeholder="password"
                    type="password"
                    name="password"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.password}
                  />
                  {touched.password && errors.password ? (
                    <div className={styles.auth_error}>{errors.password}</div>
                  ) : null}
                  <br />
                  <br />
                  <Button
                    variant="contained"
                    color="primary"
                    disabled={!isValid}
                    type="submit"
                  >
                    Login
                  </Button>
                  <br />
                  <br />
                  <span
                    className={styles.auth_text}
                    onClick={async () => {
                      dispatch(resetOpenSignIn());
                      dispatch(setOpenSignUp());
                    }}
                  >
                    You don't have a account ?
                  </span>
                </div>
              </form>
            </div>
          )}
        </Formik>
      </Modal>
    </div>
  )
}

export default Auth
