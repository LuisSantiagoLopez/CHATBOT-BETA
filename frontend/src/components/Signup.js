import React, { useState, useEffect } from "react";
import api from "./api";
import { Link } from "react-router-dom";

export default function Signup() {
  const [userData, setUserData] = useState({
    email: "",
    password: "",
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);

  const handleInputChange = (field, value) => {
    setUserData((prevUserData) => ({ ...prevUserData, [field]: value }));
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  useEffect(() => {
    if (isSubmitted && !isRegistered) {
      api
        .post("/user_management/signup/", userData)
        .then((response) => {
          localStorage.setItem("token", response.data.token);
          setIsRegistered(true);
        })
        .catch((error) => {
          console.log("Registration error:", error);
        });
    }
  }, [isSubmitted, isRegistered, userData]);

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
      <button onClick={handleSubmit}>Sign Up</button>
      {isRegistered && (
        <div>
          Registered successfully, Please check your email to verify your
          account.
        </div>
      )}
      <Link to="/">Return to Main Menu</Link>
    </div>
  );
}
