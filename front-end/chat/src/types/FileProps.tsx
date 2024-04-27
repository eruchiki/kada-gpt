import * as React from "react";

type FilePropsType = {
  setData: React.Dispatch<React.SetStateAction<File[]>>;
  fileList: File[]
};

export default FilePropsType;
