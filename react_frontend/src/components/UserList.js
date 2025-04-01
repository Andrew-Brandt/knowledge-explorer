import React from "react";
import { useUsers } from "../hooks/useUsers";

const UserList = () => {
  const { data: users, isLoading, isError, error } = useUsers();

  if (isLoading) {
    return <p className="text-center text-gray-500">Loading users...</p>;
  }

  if (isError) {
    return <p className="text-center text-red-500">Error: {error.message}</p>;
  }

  return (
    <div className="overflow-x-auto mt-6 border border-gray-300 dark:border-gray-700 rounded-lg">
      <table className="min-w-full text-sm bg-white dark:bg-gray-800">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-700 text-left text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-300">
            <th className="px-4 py-3">ID</th>
            <th className="px-4 py-3">Username</th>
            <th className="px-4 py-3">Email</th>
            <th className="px-4 py-3">Admin</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr
              key={user.id}
              className="border-t border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <td className="px-4 py-3">{user.id}</td>
              <td className="px-4 py-3">{user.username}</td>
              <td className="px-4 py-3">{user.email}</td>
              <td className="px-4 py-3">{user.is_admin ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;
