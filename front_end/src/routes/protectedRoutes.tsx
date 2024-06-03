import { lazy } from "react";
import Test from "src/app/test";
import SuspenseWrapper from "src/components/suspenseWrapper";
const Home = SuspenseWrapper(lazy(() => import("src/app/home")));
// const Test = SuspenseWrapper(lazy(() => import("src/app/test")));
import MainLayout from "src/layout/mainLayout";

const ProtectedRoutes = {
  path: "/",
  element: <MainLayout />,
  children: [
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "/test",
      element: <Test />,
    },
  ],
};

export default ProtectedRoutes;
