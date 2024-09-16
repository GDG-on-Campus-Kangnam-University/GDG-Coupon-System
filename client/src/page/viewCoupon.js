import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import gdsc from "../assets/gdsc.png";
import './viewCoupon.css'; // 위의 CSS를 적용하기 위해 import

// API로부터 쿠폰 목록을 가져오는 함수
const fetchCoupons = async (userId, isUsedFilter) => {
  try {
    const url = isUsedFilter !== null
      ? `http://localhost:8000/api/coupon/list?user_id=${userId}&is_used=${isUsedFilter}`
      : `http://localhost:8000/api/coupon/list?user_id=${userId}`;
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch coupons");
    }

    const data = await response.json();
    return data.coupons;
  } catch (error) {
    console.error(error);
    return [];
  }
};

const ViewCoupons = ({ user }) => {
  const navigate = useNavigate();
  const [coupons, setCoupons] = useState([]);
  const [isUsedFilter, setIsUsedFilter] = useState(null);  // 필터: 사용되지 않은 쿠폰 / 사용된 쿠폰

  // 쿠폰 목록을 가져오는 useEffect
  useEffect(() => {
    const loadCoupons = async () => {
      const coupons = await fetchCoupons(user.id, isUsedFilter);
      setCoupons(coupons);
    };

    loadCoupons();
  }, [user.id, isUsedFilter]); // 필터가 바뀔 때마다 다시 쿠폰을 가져옴

  // 사용되지 않은 쿠폰과 사용된 쿠폰을 필터링하는 함수
  const handleFilterChange = (e) => {
    const value = e.target.value;
    setIsUsedFilter(value === "all" ? null : value === "used");
  };


  return (
    <div className="coupon-container">
      <div className="link" onClick={()=>navigate("/")}>
        <img src={gdsc} alt="gdsc" className="gdsc" />
      </div>
      <h2>{user.name}의 쿠폰 목록</h2>

      {/* 필터 선택 박스 */}
      <div className="filter-container">
        <label htmlFor="filter">쿠폰 필터: </label>
        <select id="filter" onChange={handleFilterChange}>
          <option value="all">모두 보기</option>
          <option value="unused">사용되지 않은 쿠폰</option>
          <option value="used">사용된 쿠폰</option>
        </select>
      </div>

      {/* 쿠폰 목록을 표 형태로 표시 */}
      <table className="coupon-table">
        <thead>
          <tr>
            <th>발급한 사용자</th>
            <th>쿠폰 번호</th>
            <th>할인 금액</th>
            <th>사용 여부</th>
          </tr>
        </thead>
        <tbody>
          {coupons.length > 0 ? (
            coupons.map((coupon, index) => (
              <tr key={index}>
                <td>
                    {coupon.create_user_name}
                </td>
                <td>
                    {coupon.coupon_number}
                </td>
                <td>{coupon.discount_price}원</td>
                <td>{coupon.is_used ? "사용됨" : "사용되지 않음"}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3">쿠폰이 없습니다.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};
export default ViewCoupons;
