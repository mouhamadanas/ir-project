import { useDispatch } from "react-redux";
import { AppDispatch } from "src/reduxConfig/store";

export const useAppDispatch: () => AppDispatch = useDispatch;
