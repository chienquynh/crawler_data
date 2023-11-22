import React from 'react'
import { useSelector } from 'react-redux'
import { Route, Navigate } from 'react-router-dom'

const PublicRoute = ({ ...routeProps }) => {
  console.log(routeProps);
  const { isAuth } = useSelector((state) => state.auth)
  return <>{isAuth ? <Navigate to="/app" /> : <Route {...routeProps} />}</>
}

export default PublicRoute
