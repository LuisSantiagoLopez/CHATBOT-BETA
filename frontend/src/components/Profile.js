import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "./api";

export default function Profile() {
  const [userData, setUserData] = useState({ email: "", password: "" });

  useEffect(() => {
    const token = localStorage.getItem("token"); // Retrieve the token from local storage
    api
      .get("/user_management/profile/", {
        headers: { Authorization: `Token ${token}` }, // Include the token in request header
      })
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        console.log("Error fetching profile:", error);
      });
  }, []);

  return (
    <div>
      <h1>User Profile</h1>
      <p>
        <strong>Email:</strong> {userData.email}
      </p>
      <p>
        <strong>Password:</strong> {userData.password}
      </p>
      <Link to="/">Return to Main Menu</Link>
    </div>
  );
}
