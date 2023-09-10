import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Navbar = ({ logout }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  // Update the state whenever local storage changes
  useEffect(() => {
    const handleStorageChange = () => {
      setIsLoggedIn(!!localStorage.getItem("token"));
    };

    // Listen for changes to local storage
    window.addEventListener("storage", handleStorageChange);

    // Cleanup: remove the event listener when the component unmounts
    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false); // Update the state to re-render the component
  };

  return (
    <nav>
      <ul>
        {!isLoggedIn ? (
          <>
            <li>
              <Link to="/signup">Sign Up</Link>
            </li>
            <li>
              <Link to="/signin">Sign In</Link>
            </li>
          </>
        ) : (
          <li>
            <Link to="/" onClick={handleLogout}>
              Log Out
            </Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
