import React from "react";
import axios from "axios";

export default function Logout() {
  const handleLogout = async () => {
    const res = await axios.post("/api/user_management/user_logout/");
    console.log(res.data);
  };

  return <button onClick={handleLogout}>Logout</button>;
}
