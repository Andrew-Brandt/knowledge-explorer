import { useQuery } from "@tanstack/react-query";

export const useUsers = () => {
  return useQuery({
    queryKey: ["users"],
    queryFn: async () => {
      const res = await fetch("http://localhost:5000/admin/users", {
        credentials: "include",
      });
      if (!res.ok) {
        const error = await res.text();
        throw new Error(error || "Failed to fetch users");
      }
      return res.json();
    },
  });
};
