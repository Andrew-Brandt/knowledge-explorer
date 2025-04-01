import React from "react";
import { useUser } from "../hooks/useAuth";
import UserList from "../components/UserList";

const AdminDashboard = () => {
  const { data: user } = useUser();

  return (
    <div className="max-w-5xl mx-auto py-16 px-4">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <p className="mb-6">
        Welcome, <strong>{user.username}</strong>!
      </p>

      <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-6 bg-white dark:bg-gray-800 mb-10">
        <h2 className="text-xl font-semibold mb-2">System Overview</h2>
        <p className="text-gray-700 dark:text-gray-300">
          Here you can manage backend tools, moderate content, view user
          activity, or build tools to edit the Knowledge Graph.
        </p>
      </div>

      <UserList />
    </div>
  );
};

export default AdminDashboard;
