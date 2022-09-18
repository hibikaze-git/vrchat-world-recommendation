import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux';
import Auth from '../auth/Auth';
import { AppDispatch } from '../../app/store';
import { getSession, getCSRF, selectIsAuthenticated, fetchAsyncLogout, whoami } from '../auth/authSlice';

const Core: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();

  const isAuthenticated = useSelector(selectIsAuthenticated);

  useEffect(() => {
    dispatch(getSession());
    dispatch(getCSRF());
  }, []);

  if (!isAuthenticated) {
    return (
      <div>
        not log in
        <Auth />
      </div>
    );
  }

  return (
    <div>
      <div className="container mt-3">
        <h1>React Cookie Auth</h1>
        <p>You are logged in!</p>
        <button className="btn btn-primary mr-2" onClick={() => dispatch(whoami())}>WhoAmI</button>
        <button className="btn btn-danger" onClick={() => dispatch(fetchAsyncLogout())}>Log out</button>
      </div>
    </div>
  )
}

export default Core