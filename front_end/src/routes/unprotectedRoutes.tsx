import Login from "src/app/login";
import AuthLayout from "src/layout/authLayout";

const UnprotectedRoutes = {
  path: "/login",
  element: <AuthLayout />,
  children: [
    {
      path: "/login",
      element: <Login />,
    },
  ],
};
export default UnprotectedRoutes;
