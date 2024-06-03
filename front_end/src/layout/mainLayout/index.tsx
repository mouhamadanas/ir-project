import { useEffect } from "react";
import { Navigate, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAppSelector } from "src/hooks/useAppSelector";

const MainLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { token } = useAppSelector((state) => state.auth);

  // useEffect(() => {
  //   if (!token) navigate("/login", { replace: true });
  // }, [location.pathname]);

  // if (!token) return <Navigate to="/login" replace />;
  return (
    <div>
      
      <Outlet />
    </div>
  );
};

export default MainLayout;
