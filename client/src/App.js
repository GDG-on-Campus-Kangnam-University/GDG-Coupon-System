import React, { useState } from "react";
import Home from "./page/home";
import Login from "./page/login";

const App = () => {
  const [userId, setUserId] = useState(null);

  return (
    <div>
      {!userId ? <Login setUserId={setUserId} /> : <Home userId={userId} />}
    </div>
  );
};

export default App;
