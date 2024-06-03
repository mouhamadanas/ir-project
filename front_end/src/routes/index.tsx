import { useRoutes } from "react-router-dom";
import ProtectedRoutes from "./protectedRoutes";
import UnprotectedRoutes from "./unprotectedRoutes";

function Routes() {
  return useRoutes([ProtectedRoutes, UnprotectedRoutes]);
}
export default Routes;
