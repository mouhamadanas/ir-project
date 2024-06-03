const errorCode: any = {};

export const getErrorMessageFromCode = (code: number) => {
  const message: string = errorCode[code];
  return message ? message : errorCode["error"];
};
