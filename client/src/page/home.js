import React, { useState } from "react";
import "../App.css";

const Home = ({ userId }) => {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [coupons, setCoupons] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://3.39.110.98:8000/api/coupon/create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: userId, email, name }),
        }
      );

      if (!response.ok) {
        throw new Error("쿠폰 생성 실패");
      }

      const responseData = await response.json();

      setCoupons([...coupons, { number: responseData.coupon_number, email }]);
    } catch (e) {
      alert("더이상 쿠폰을 생성할 수 없습니다.");
    }
  };

  return (
    <div className="home-container">
      <img src="/gdsc.png" alt="gdsc" className="gdsc" />
      <h2>쿠폰 생성기</h2>
      <form onSubmit={handleSubmit} className="home-form">
        <div className="input-group">
          <label htmlFor="name">이름</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="email">이메일</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">쿠폰 생성</button>
        <div className="coupon-list">
          {coupons.map((coupon, index) => (
            <p key={index} className="coupon-item">
              {coupon.number}
            </p>
          ))}
        </div>
      </form>
      <div>
        <img src="/keroro6.png" alt="keroro" className="image" />
      </div>
    </div>
  );
};

export default Home;
