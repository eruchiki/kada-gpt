import axios from "axios";

const GetChatHistory = (userid: number, threadid: number) => {
  const url = `${process.env.API_URL}/chat/users/${userid}/thread/${threadid}`;
  const userlist = axios.get(url);
  return userlist;
};

export default GetChatHistory;
