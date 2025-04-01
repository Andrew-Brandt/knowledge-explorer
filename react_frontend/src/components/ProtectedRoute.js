import React from "react";
import { Navigate } from "react-router-dom";
import { useUser } from "../hooks/useAuth";

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { data: user, isLoading } = useUser();

  if (isLoading) return <p className="text-center py-8">Loading...</p>;

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user.is_admin) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
