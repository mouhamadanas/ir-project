const errorCode: Array<number> = [];
const handleErrorTokenFromErrorCode = (code: number) => {
  return errorCode.includes(code);
};

export default handleErrorTokenFromErrorCode;
