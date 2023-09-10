import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from "./api";

export default function Login() {
  const [userData, setUserData] = useState({
    email: "",
    password: "",
  });

  const handleInputChange = (field, value) => {
    setUserData((prevUserData) => ({ ...prevUserData, [field]: value }));
  };

  const login = () => {
    api
      .post("/user_management/signin/", userData)
      .then((response) => {
        localStorage.setItem("token", response.data.token);
        alert("Login successful");
      })
      .catch((error) => {
        alert("Invalid credentials");
      });
  };

  return (
    <div>
      <input
        value={userData.email}
        onChange={(e) => handleInputChange("email", e.target.value)}
      />
      <input
        value={userData.password}
        onChange={(e) => handleInputChange("password", e.target.value)}
      />
      <button onClick={login}>Sign In</button>
      <Link to="/">Return to Main Menu</Link>
    </div>
  );
}
