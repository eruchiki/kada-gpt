import axios from "axios";

const GetUserList = () => {
  const url = `${process.env.API_URL}/chat/users`;
  const userlist = axios.get(url)
  return userlist
}

export default GetUserList;