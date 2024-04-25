import MessagePropsType from "../../src/types/MessageProps";
import axios from "axios";

const SendMessage = (data:MessagePropsType) => {
  const url = `${process.env.HOST_URL}/chat/users/${data.create_user_id}/thread/${data.thread_id}`;
  const response = axios.post(url,data);
  return response;
};

export default SendMessage;
