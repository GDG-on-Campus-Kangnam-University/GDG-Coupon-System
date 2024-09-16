// src/components/Home.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import gdsc from "../assets/gdsc.png";

const Home = ({user}) => {
  const navigate = useNavigate();
  const [isSending, setIsSending] = useState(false); // 상태 관리: 요청 중인지 확인


  const handleCreateCoupon = () => {
    navigate('/create-coupon');
  };

  const handleViewCoupons = () => {
    navigate('/view-coupons');
  };

  const handleSendMail = async () => {
    if (isSending) {
      alert("메일 발송 중입니다. 잠시만 기다려주세요.");
      return; // 연속 클릭 방지
    }

    setIsSending(true); // 요청 중임을 상태에 반영
    try {
      const response = await fetch(`http://3.39.110.98:8000/update-sheets?user_id=${user.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = await response.json(); // 응답 데이터를 JSON으로 변환

      if (!response.ok) {
        throw new Error(result.detail || "메일 발송에 실패했습니다."); // 서버에서 제공한 오류 메시지를 출력
      }

      alert(result.message); // 성공 메시지 출력
    } catch (error) {
      alert(`메일 발송 실패: ${error.message}`); // 실패 원인 메시지 출력
    } finally {
      setIsSending(false); // 요청 완료 후 상태를 되돌림
    }
  };

  return (
    <div style={styles.container}>
      <img src={gdsc} alt="gdsc" className="gdsc" />
      <h1>홈 화면</h1>
      <p>{user.name}님 어서오세요!</p>
      <div style={styles.buttonContainer}>
        <button style={styles.button} onClick={handleCreateCoupon}>
          쿠폰 생성하기
        </button>
        <button style={styles.button} onClick={handleViewCoupons}>
          전체 생성된 쿠폰 DB 확인하기
        </button>
        <button
          style={{ ...styles.button, backgroundColor: isSending ? 'gray' : '#007bff' }}
          onClick={handleSendMail}
          disabled={isSending} // 요청 중이면 버튼 비활성화
        >
          {isSending ? '메일 발송 중...' : 'Mail 발송 실행하기'}
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    textAlign: 'center',
    paddingTop: '50px',
    display:'flex',
    flexDirection:'column',
    alignItems:'center',
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    marginTop: '30px',
    alignItems: 'center',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
    width: '250px',
  },
};

export default Home;
