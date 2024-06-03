// @ts-ignore
import {
  Autocomplete,
  Box,
  Container,
  Tab,
  Tabs,
  TextField,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import GenericButton from "src/components/generic-button";
import {
  useGetResultWithoutClusterMutation,
  useGetSuggestMutation,
} from "./services/api";

const Home = () => {
  const [tabs, settabs] = useState("wikir");
  const [searchInput, setsearchInput] = useState("");
  const [suggestions, setsuggestions] = useState([]);
  const [data, setData] = useState({
    top_matches_scores: [],
    top_matching_documents: [],
  });
  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    settabs(newValue);
  };
  const [getSuggestion, { isLoading }] = useGetSuggestMutation();
  const [getQuery, { isLoading: loadingDara }] =
    useGetResultWithoutClusterMutation();
  useEffect(() => {
    const timeout = setTimeout(() => {
      getSuggestion({ data: tabs, query: searchInput })
        .unwrap()
        .then((data) => {
          setsuggestions(data.suggestions);
        });
    }, 1000);
    return () => clearTimeout(timeout);
  }, [searchInput]);
  return (
    <Box sx={{ margin: "100px auto", bgcolor: "background.50" }}>
      <Container maxWidth="lg">
        <Tabs
          variant="fullWidth"
          value={tabs}
          onChange={handleChange}
          aria-label="disabled tabs example"
        >
          <Tab label="wikir" value="wikir" />
          <Tab label="antique" value="antique" />
        </Tabs>
        <Box sx={{ mt: 4, textAlign: "center" }}>
          <Autocomplete
            onInputChange={(e, value) => {
              setsearchInput(value);
            }}
            freeSolo
            fullWidth
            disablePortal
            id="combo-box-demo"
            options={suggestions}
            // sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label={tabs} />}
          />
          {isLoading && <div>loading...</div>}
        </Box>
        <Box sx={{ mt: 4, textAlign: "center" }}>
          <GenericButton
            loading={loadingDara}
            title="search"
            sx={{ maxWidth: "300px" }}
            onClick={() => {
              getQuery({ data: tabs, query: searchInput })
                .unwrap()
                .then((data: any) => {
                  setData(data);
                });
            }}
          />
        </Box>
        {data.top_matching_documents.map((doc, i) => (
          <>
            <Box sx={{ display: "flex", gap: "10px" }}>
              <Box> score:{data.top_matches_scores[i]}</Box>
              <Box> document:{doc}</Box>
            </Box>
          </>
        ))}
      </Container>
    </Box>
  );
};

export default Home;
