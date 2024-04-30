import CreateThread from "../../../app/api/CreateThread";
import ThreadCreatePropsType from "../../types/ThreadCreateProps";
import Button from "@mui/material/Button";

const ThreadButton = (props: ThreadCreatePropsType) => {
  return (
    <Button
      onClick={(e) => {
        CreateThread(props.userid, props.ThreadInfo, e);
      }}
    />
  );
};

export default ThreadButton;
