import ChatFunction from "../../../app/api/ChatAPI";
import ChatPropsType from "../../types/ChatProps";


const SendButton = (props: ChatPropsType) => {
  return (
    <button
      id="submit-button"
      // className={isLoading ? "loading" : ""}
      onClick={() =>
        ChatFunction(props)
      }
    ></button>
  );
};

export default SendButton