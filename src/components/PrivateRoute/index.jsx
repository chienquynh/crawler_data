import React from 'react'
import { useSelector } from 'react-redux'
import { Route, Navigate } from 'react-router-dom'

const PrivateRoute = ({ ...routeProps }) => {
  const { isAuth } = useSelector((state) => state.auth)
  return (
    <>
      {!isAuth && <Navigate to="/login" />}

      {isAuth && <Route {...routeProps} />}
    </>
  )
}

export default PrivateRoute
