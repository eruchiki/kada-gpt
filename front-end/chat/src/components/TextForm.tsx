import React from "react";
import { TextField } from "@mui/material";
import TextFormPropsType from "../types/FormProps";

const TextForm = (props: TextFormPropsType) => {
  return (
    <TextField
      id="outlined-basic"
      label={props.title}
      variant="outlined"
      defaultValue={props.data}
      onChange={(e) => props.setData(e.target.value)}
    />
  );
};

export default TextForm;
