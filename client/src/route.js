import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Coupon from './page/coupon'
import Home from './page/home'
import ViewCoupons from './page/viewCoupon'

const HomeRoute = ({user}) => {
  return (
    <Routes>
      <Route path="/" element={<Home user={user}/>} />
      <Route path="/create-coupon" element={<Coupon user={user}/>} />
      <Route path="/view-coupons" element={<ViewCoupons user={user} />} />
  </Routes>
  )
}

export default HomeRoute