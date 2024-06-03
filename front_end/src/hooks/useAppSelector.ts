import { TypedUseSelectorHook, useSelector } from "react-redux";
import { RootState } from "src/reduxConfig/store";

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
