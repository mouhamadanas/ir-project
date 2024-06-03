import i18next from "i18next";

const useGetIsRtlDirection = () => {
  return i18next.language === "ar";
};

export default useGetIsRtlDirection;
