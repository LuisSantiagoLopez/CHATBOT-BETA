import React, { useEffect } from "react";
import api from "./api";
import { Link } from "react-router-dom";

const VerifyEmail = ({ match }) => {
  const { token } = match.params;

  useEffect(() => {
    api
      .get(`/user_management/verify-email/${token}/`)
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert("An error occurred during email verification.");
      });
  }, [token]);

  return (
    <div>
      <h1>Verifying your email...</h1>
      <Link to="/">Return to Main Menu</Link>
    </div>
  );
};

export default VerifyEmail;
