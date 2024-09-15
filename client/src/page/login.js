import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

const Login = ({ setUserId }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const navigate = useNavigate();

  const images = [
    "/keroro1.png",
    "/keroro2.png",
    "/keroro3.png",
    "/keroro4.png",
    "/keroro5.png",
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://3.39.110.98:8000/api/user/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        throw new Error("로그인 실패");
      }

      const data = await response.json();
      setUserId(data.id);

      navigate("/");
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000); // 이미지 변경 주기 (3초)

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="login-container">
      <img src="/gdsc.png" alt="gdsc" className="gdsc" />
      <h2>로그인</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="input-group">
          <label htmlFor="email">아이디</label>
          <input
            type="text"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="password">비밀번호</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">로그인</button>
      </form>
      <img src={images[currentImageIndex]} alt="keroro" className="image" />
    </div>
  );
};

export default Login;
