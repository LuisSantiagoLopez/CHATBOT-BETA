import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login.js";
import Logout from "./components/Logout";
import Subscription from "./components/Subscription";
import Profile from "./components/Profile";
import MainMenu from "./components/MainMenu";
import VerifyEmail from "./components/VerifyEmail";
import Navbar from "./components/Navbar";

function App() {
  const logout = () => {
    localStorage.removeItem("token");
  };

  return (
    <BrowserRouter>
      <Navbar logout={logout} />
      <Routes>
        <Route path="/" element={<MainMenu />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/signin" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/verify-email/:token" component={VerifyEmail} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
