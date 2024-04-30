import axios from "axios";

const GetChatHistory = async (userid: number, threadid: number) => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users/${userid}/thread/${threadid}/history`;
  return await axios
    .get(url)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

export default GetChatHistory;
