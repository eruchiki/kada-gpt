import { React, useState } from "react";
import { TextField, FormHelperText, FormControl } from "@mui/material";
import TextFormPropsType from "../types/FormProps";

const TextForm = (props: TextFormPropsType) => {
  const [selectError, setSelectError] = useState<string>();
  return (
    <FormControl error={!!selectError} sx={{ minWidth: 500 }}>
      <TextField
        id="outlined-basic"
        label={props.title}
        variant="outlined"
        defaultValue={props.data}
        fullWidth
        onChange={(e) => props.setData(e.target.value)}
      />
    </FormControl >
  );
};

export default TextForm;
