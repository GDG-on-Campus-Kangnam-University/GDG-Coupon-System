import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";
import gdsc from "../assets/gdsc.png";
import keroro from "../assets/keroro6.png";

const Coupon = ({ user }) => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [coupons, setCoupons] = useState([]);
  const [isSending, setIsSending] = useState(false); // 상태 관리: 요청 중인지 확인


  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        const response = await fetch(
          `http://3.39.110.98/api/coupon/user/${user.id}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error("쿠폰 조회 실패");
        }

        const responseData = await response.json();
        console.log(responseData)

        // 쿠폰 목록을 추가
        setCoupons(responseData.coupons);

      } catch (e) {
        alert("쿠폰을 가져오는 데 실패했습니다.");
      }
    };

    fetchCoupons();
  }, []); 
  

  const handleSubmit = async (e) => {
    if (isSending) {
      alert("메일 발송 중입니다. 잠시만 기다려주세요.");
      return; // 연속 클릭 방지
    }
    console.log(user.role)
    
    e.preventDefault();
    if(user.role ==="CoreMember" && (email !== user.email || name !== user.name)){
      alert("올바른 본인의 이름과 이메일을 입력해주세요.");
      return;
    }
    setIsSending(true); 

    try {
      const response = await fetch(
        "http://3.39.110.98/api/coupon/create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: user.id, email, name }),
        }
      );

      if (!response.ok) {
        throw new Error("쿠폰 생성 실패");
      }

      const responseData = await response.json();

      setCoupons((prevCoupons) => [...prevCoupons, responseData.coupon_number]);
    } catch (e) {
      alert("더 이상 쿠폰을 생성할 수 없습니다.");
    } finally{
      setIsSending(false)
    }
  };

  return (
    <div className="home-container">
      <div className="link" onClick={()=>{navigate('/')}}>
        <img src={gdsc} alt="gdsc" className="gdsc" />
      </div>
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
        <button
          style={{ backgroundColor: isSending ? 'gray' : '#007bff' }}
          disabled={isSending}
          type="submit">{isSending ? "쿠폰 발급 중" :"쿠폰 생성"}</button>
        <div className="coupon-list">
          {coupons?.map((coupon, index) => (
            <p key={index} className="coupon-item">
              {coupon}
            </p>
          ))}
        </div>
      </form>
      <div>
        <img src={keroro} alt="keroro" className="image" />
      </div>
    </div>
  );
};

export default Coupon;
