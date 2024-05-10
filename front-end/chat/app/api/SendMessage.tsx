import MessagePropsType from "../../src/types/MessageProps";
import axios from "axios";

const SendMessage = async (data: MessagePropsType) => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users/${data.create_user_id}/thread/${data.thread_id}`;
  return await axios
    .post(url, data)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

export default SendMessage;
