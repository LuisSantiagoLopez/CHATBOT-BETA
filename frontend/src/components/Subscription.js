import React from "react";
import axios from "axios";

export default function Subscription() {
  const handleSubscription = async () => {
    const paymentMethod = "your_stripe_payment_method_id";
    const res = await axios.post("/api/user_management/create_subscription/", {
      payment_method: paymentMethod,
    });
    console.log(res.data);
  };

  return <button onClick={handleSubscription}>Subscribe</button>;
}
