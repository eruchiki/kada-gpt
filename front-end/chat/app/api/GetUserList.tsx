import axios from "axios";

const GetUserList = () => {
  const url = `${process.env.HOST_URL}/users`;
  const userlist = axios.get(url)
  return userlist
}

export default GetUserList;