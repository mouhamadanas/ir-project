import { Box } from "@mui/material";
import { useGetTestQuery } from "./services/api";
import { containerStyles } from "./styles";
import { Link } from "react-router-dom";

const Test = () => {
  const { data, isFetching, isError, error } = useGetTestQuery("10");

  return (
    <Box sx={containerStyles}>
      {isFetching && "loading..."}
      {isError && JSON.stringify(error)}
      {JSON.stringify(data)}
      <Link to="/">home</Link>
    </Box>
  );
};

export default Test;
