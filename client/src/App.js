import React, { useState } from "react";
import Login from "./page/login";
import HomeRoute from "./route";

const App = () => {
  const [user, setUser] = useState(null);

  return (
    <div>
      {!user ? <Login setUser={setUser} /> : <HomeRoute user={user} />}
    </div>
  );
};

export default App;
